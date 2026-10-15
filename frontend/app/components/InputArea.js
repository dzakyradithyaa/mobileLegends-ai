"use client";
import React, { useRef } from "react";
import { Upload, Camera, Scan } from "lucide-react";

export default function InputArea({ onFileChange, onSnap, disabled }) {
  const fileInputRef = useRef(null);

  const handleUploadClick = () => {
    if (!disabled) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="w-full">
      {/* Hidden File Input */}
      <input
        type="file"
        accept="image/*"
        onChange={onFileChange}
        className="hidden"
        ref={fileInputRef}
        disabled={disabled}
      />

      {/* Instructions Card */}
      <div className="glass-mlbb card-mlbb rounded-xl p-6 border border-blue-500/20 mb-6">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-lg bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-600/40">
            <Scan className="w-6 h-6 text-white" />
          </div>

          <div>
            <h3 className="text-lg font-bold text-white mb-2 tracking-wide">
              HERO DETECTION
            </h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Upload a hero image or capture directly from the camera. Our AI
              will analyze and classify the hero with role identification.
            </p>
          </div>
        </div>
      </div>

      {/* Buttons */}
      <div className="grid grid-cols-1 gap-4 mb-6">
        {/* Upload Button */}
        <button
          onClick={handleUploadClick}
          disabled={disabled}
          className={`
            btn-mlbb
            px-6 py-6 rounded-xl font-semibold
            transition-all duration-300
            flex items-center gap-4
            ${
              disabled
                ? "bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700"
                : "glass-mlbb border border-blue-500/30 hover:border-blue-400 text-white neon-blue"
            }
          `}
        >
          <div
            className={`p-3 rounded-lg shadow ${
              disabled ? "bg-slate-700" : "bg-blue-600 shadow-blue-600/30"
            }`}
          >
            <Upload
              className={`w-6 h-6 ${
                disabled ? "text-slate-500" : "text-white"
              }`}
            />
          </div>

          <div className="text-left flex-1">
            <div className="text-lg font-bold">
              {disabled ? "PROCESSING..." : "UPLOAD IMAGE"}
            </div>
            <div
              className={`text-xs mt-1 ${
                disabled ? "text-slate-600" : "text-slate-400"
              }`}
            >
              Select from your device
            </div>
          </div>
        </button>

        {/* Camera Button */}
        <button
          onClick={onSnap}
          disabled={disabled}
          className={`
            btn-mlbb
            px-6 py-6 rounded-xl font-semibold
            transition-all duration-300
            flex items-center gap-4
            ${
              disabled
                ? "bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700"
                : "glass-mlbb border border-blue-500/30 hover:border-blue-400 text-white neon-blue"
            }
          `}
        >
          <div
            className={`p-3 rounded-lg shadow ${
              disabled ? "bg-slate-700" : "bg-blue-600 shadow-blue-600/30"
            }`}
          >
            <Camera
              className={`w-6 h-6 ${
                disabled ? "text-slate-500" : "text-white"
              }`}
            />
          </div>

          <div className="text-left flex-1">
            <div className="text-lg font-bold">CAMERA CAPTURE</div>
            <div
              className={`text-xs mt-1 ${
                disabled ? "text-slate-600" : "text-slate-400"
              }`}
            >
              Capture in real-time
            </div>
          </div>
        </button>
      </div>

      {/* Status */}
      <div className="text-center">
        {disabled ? (
          <div className="glass-mlbb inline-flex items-center gap-3 px-5 py-3 rounded-full border border-blue-500/30 neon-blue">
            <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-blue-300 font-semibold uppercase tracking-wide">
              Analyzing Hero...
            </span>
          </div>
        ) : (
          <div className="glass-mlbb inline-flex items-center gap-2 px-4 py-2 rounded-full border border-blue-500/20">
            <span className="text-xs text-slate-400 uppercase tracking-wide">
              Supported: JPG, PNG, WEBP | Max: 10MB
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
