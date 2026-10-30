export const ACTIVE_RATIO = 0.45;

export function selectActiveProjectId(
  ratios: Map<string, number>,
  failed: Record<string, boolean>,
  threshold = ACTIVE_RATIO,
): string | null {
  let bestId: string | null = null;
  let bestRatio = 0;

  ratios.forEach((ratio, id) => {
    if (failed[id]) return;
    if (ratio > bestRatio) {
      bestRatio = ratio;
      bestId = id;
    }
  });

  return bestId && bestRatio >= threshold ? bestId : null;
}
