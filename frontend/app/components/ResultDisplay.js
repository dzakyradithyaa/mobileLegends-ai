"use client";
import Image from "next/image";
import {
  CheckCircle2,
  Loader2,
  AlertTriangle,
  Award,
  Target,
} from "lucide-react";

export default function ResultDisplay({
  previewUrl,
  prediction,
  isScanning,
  heroConfidence,
}) {
  const roleConfig = {
    Fighter: { label: "Fighter" },
    Marksman: { label: "Marksman" },
    Mage: { label: "Mage" },
    Assassin: { label: "Assassin" },
    Tank: { label: "Tank" },
    Support: { label: "Support" },
  };

  const confidencePercent = heroConfidence
    ? (heroConfidence * 100).toFixed(1)
    : "0";

  const roleLabel =
    prediction && prediction.role
      ? roleConfig[prediction.role]?.label
      : "Unknown";

  return (
    <div className="w-full">
      <div className="bg-[#0a0a0f] border border-blue-500/30 rounded-xl p-6 space-y-6 shadow-[0_0_20px_rgba(0,80,255,0.12)]">
        {/* STATUS BAR */}
        <div className="flex items-center gap-3 pb-5 border-b border-blue-500/20">
          {isScanning ? (
            <>
              <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
              <p className="text-[11px] text-blue-400 tracking-widest font-semibold uppercase">
                Analyzing
              </p>
            </>
          ) : prediction ? (
            <>
              <CheckCircle2 className="w-5 h-5 text-blue-300" />
              <p className="text-[11px] text-blue-300 tracking-widest font-semibold uppercase">
                Detection Complete
              </p>
            </>
          ) : (
            <>
              <AlertTriangle className="w-5 h-5 text-blue-500/40" />
              <p className="text-[11px] text-blue-500/40 tracking-widest font-semibold uppercase">
                Awaiting Input
              </p>
            </>
          )}
        </div>

        {/* MAIN GRID */}
        <div className="grid grid-cols-2 gap-5">
          {/* INPUT IMAGE */}
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <Target className="w-4 h-4 text-blue-400" />
              <span className="text-xs text-blue-400/80 uppercase tracking-wide">
                Input
              </span>
            </div>

            <div
              className={`relative w-full aspect-square rounded-lg border border-blue-500/30 bg-[#0c0c12] overflow-hidden flex items-center justify-center`}
            >
              {previewUrl ? (
                <Image
                  src={previewUrl}
                  alt="Preview"
                  fill
                  className="object-cover"
                />
              ) : (
                <AlertTriangle className="w-10 h-10 text-blue-500/30" />
              )}
            </div>
          </div>

          {/* RESULTS */}
          {!prediction ? (
            <div className="flex items-center justify-center text-blue-500/30 text-xs">
              Upload image to detect hero
            </div>
          ) : (
            <div className="flex flex-col gap-5">
              {/* HERO INFO (NO IMAGE) */}
              <div className="border border-blue-500/20 rounded-lg p-4 bg-[#0c0c12] space-y-3 shadow-[0_0_12px_rgba(0,80,255,0.05)]">
                <div className="flex items-center gap-2">
                  <Award className="w-4 h-4 text-blue-400/80" />
                  <span className="text-[11px] text-blue-400/70 uppercase tracking-widest">
                    Detection
                  </span>
                </div>

                <p className="text-2xl font-bold text-white tracking-wide">
                  {prediction.hero}
                </p>

                <div className="inline-flex px-3 py-1 rounded-md border border-blue-500/30 text-blue-300 text-xs font-semibold tracking-wide uppercase">
                  {roleLabel}
                </div>
              </div>

              {/* CONFIDENCE */}
              <div className="border border-blue-500/20 rounded-lg p-4 bg-[#0c0c12] space-y-3 shadow-[0_0_12px_rgba(0,80,255,0.05)]">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] text-blue-400/70 uppercase tracking-widest">
                    Confidence
                  </span>
                  <span className="text-lg font-bold text-blue-300">
                    {confidencePercent}%
                  </span>
                </div>

                <div className="w-full h-2 bg-blue-500/20 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-400 transition-all duration-700"
                    style={{
                      width: `${Math.min(parseFloat(confidencePercent), 100)}%`,
                    }}
                  ></div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
