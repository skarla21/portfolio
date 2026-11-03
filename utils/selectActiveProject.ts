/** Wake IntersectionObserver near the old play threshold. */
export const ACTIVE_RATIO = 0.25;

/**
 * Pick the most visible stage. Any positive intersection wins so reverse
 * scroll does not sit on a poster while waiting for 25% coverage.
 * `previousId` sticks while fully in a gap between panels.
 */
export function selectActiveProjectId(
  ratios: Map<string, number>,
  failed: Record<string, boolean>,
  previousId: string | null = null,
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

  if (bestId && bestRatio > 0) return bestId;
  if (previousId && !failed[previousId]) return previousId;
  return null;
}
