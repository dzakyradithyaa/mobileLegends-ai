"use client";

import { useEffect } from "react";
import { Camera, X, Scan } from "lucide-react";

export default function CameraCapture({
  videoRef,
  canvasRef,
  onCapture,
  onClose,
  isScanning,
}) {
  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "environment" },
        });

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        }
      } catch (err) {
        console.error("Camera error:", err);
      }
    };

    startCamera();

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <div className="fixed inset-0 bg-black/80 flex flex-col items-center justify-center p-6 z-50">
      <div className="relative w-full max-w-md">
        {/* VIDEO */}
        <video
          ref={videoRef}
          className="w-full rounded-xl border border-blue-500 shadow-lg"
        />

        <canvas ref={canvasRef} className="hidden" />

        {/* CLOSE BUTTON */}
        <button
          onClick={onClose}
          className="absolute -top-4 -right-4 bg-red-500 p-2 rounded-full"
        >
          <X className="text-white w-5 h-5" />
        </button>
      </div>

      {/* CAPTURE BUTTON */}
      <button
        onClick={onCapture}
        disabled={isScanning}
        className="mt-6 bg-blue-600 text-white px-6 py-3 rounded-xl flex items-center gap-2"
      >
        <Scan className="w-5 h-5" />
        {isScanning ? "Scanning..." : "Capture"}
      </button>
    </div>
  );
}
