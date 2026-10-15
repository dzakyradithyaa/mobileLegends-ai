"use client";

import { useState, useRef } from "react";
import InputArea from "./components/InputArea";
import ResultDisplay from "./components/ResultDisplay";
import CameraCapture from "./components/CameraCapture";

import { Shield, Zap, Activity, Target } from "lucide-react";

export default function ClassifierPage() {
  const [previewUrl, setPreviewUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [heroConfidence, setHeroConfidence] = useState(null);
  const [isCameraActive, setIsCameraActive] = useState(false);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const API_URL = "http://127.0.0.1:8000/predict";

  // Toggle Camera
  const handleCameraToggle = () => {
    setIsCameraActive((prev) => !prev);
  };

  // Capture From Camera
  const handleCapture = async () => {
    if (!isCameraActive || isScanning) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) return;

      // Stop Stream After Capture
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
        setIsCameraActive(false);
      }

      const capturedFile = new File([blob], "captured_hero.jpeg", {
        type: "image/jpeg",
      });

      await processImage(capturedFile);
    }, "image/jpeg");
  };

  // Upload Image From File Picker
  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (isCameraActive && streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      setIsCameraActive(false);
    }

    await processImage(file);
  };

  // Send Image To API
  const processImage = async (file) => {
    const tempPreviewUrl = URL.createObjectURL(file);

    setPreviewUrl(tempPreviewUrl);
    setPrediction(null);
    setHeroConfidence(null);
    setIsScanning(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      setPrediction(data.prediction);
      setHeroConfidence(data.prediction.hero_confidence_score);
    } catch (error) {
      console.error("Error during prediction:", error);

      setPrediction({
        hero: "ERROR",
        role: "NETWORK_ISSUE",
        hero_confidence_score: 0,
      });

      setHeroConfidence(0);
    } finally {
      setTimeout(() => {
        setIsScanning(false);
      }, 1500);
    }
  };

  return (
    <main className="min-h-screen bg-mlbb-pattern py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header - Simple MLBB Style */}
        <div className="mb-8">
          <div className="glass-mlbb rounded-2xl p-6 border border-blue-500/20 shadow-xl">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-blue-600 rounded-xl flex items-center justify-center neon-blue">
                  <Shield className="w-7 h-7 text-white" />
                </div>

                <div>
                  <h1 className="text-3xl font-bold text-white">
                    MLBB HERO CLASSIFIER
                  </h1>
                  <p className="text-slate-400 text-sm mt-1">
                    AI-Powered Hero Detection System
                  </p>
                </div>
              </div>

              <div className="glass-mlbb px-4 py-2 rounded-lg border border-blue-500/30">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                  <span className="text-blue-400 text-sm font-semibold uppercase tracking-wide">
                    ONLINE
                  </span>
                </div>
              </div>
            </div>

            {/* Stats Bar */}
            <div className="grid grid-cols-3 gap-3 mt-6">
              <div className="glass-mlbb rounded-lg p-3 border border-blue-500/10">
                <div className="flex items-center gap-2 mb-1">
                  <Target className="w-4 h-4 text-blue-400" />
                  <span className="text-xs text-slate-400 uppercase">
                    Accuracy
                  </span>
                </div>
                <p className="text-lg font-bold text-white">95%+</p>
              </div>

              <div className="glass-mlbb rounded-lg p-3 border border-yellow-500/10">
                <div className="flex items-center gap-2 mb-1">
                  <Zap className="w-4 h-4 text-yellow-400" />
                  <span className="text-xs text-slate-400 uppercase">
                    Speed
                  </span>
                </div>
                <p className="text-lg font-bold text-white">&lt;2s</p>
              </div>

              <div className="glass-mlbb rounded-lg p-3 border border-blue-500/10">
                <div className="flex items-center gap-2 mb-1">
                  <Activity className="w-4 h-4 text-blue-400" />
                  <span className="text-xs text-slate-400 uppercase">
                    Model
                  </span>
                </div>
                <p className="text-lg font-bold text-white">CNN</p>
              </div>
            </div>
          </div>
        </div>

        {/* Layout */}
        {isCameraActive ? (
          <CameraCapture
            videoRef={videoRef}
            canvasRef={canvasRef}
            onCapture={handleCapture}
            onClose={handleCameraToggle}
            isScanning={isScanning}
          />
        ) : (
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Input Section */}
            <div className="space-y-6">
              <InputArea
                onFileChange={handleImageUpload}
                onSnap={handleCameraToggle}
                disabled={isScanning}
              />
            </div>

            {/* Results Section */}
            <div>
              <ResultDisplay
                previewUrl={previewUrl}
                prediction={prediction}
                isScanning={isScanning}
                heroConfidence={heroConfidence}
              />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
