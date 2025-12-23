"""
@Author: Alec Namey
Lego Build Time Estimator
@param piece_count: Total number of Lego pieces in the set (from API)
@param build_style: 1 = slow, 2 = normal, 3 = fast
@param distraction_level: 1–10 (1 = no distractions, 10 = very distracted)
@param organization_level: 1–10 (1 = very disorganized, 10 = very organized)
@param difficulty_level: 1–5 (1 = very easy, 5 = very difficult)
@return: (int) Estimated build time in *Minutes*
"""
def estimate_lego_build_time(
    piece_count: int,
    build_style: int,          # 1 = slow, 2 = normal, 3 = fast
    distraction_level: int,    # 1–10
    organization_level: int,   # 1–10
    difficulty_level: int      # 1–5
):
    """
    Returns estimated build time in minutes.
    """

    # --- Seconds per piece based on build style ---
    seconds_per_piece_map = {
        1: 26,  # slow
        2: 20,  # normal
        3: 14   # fast
    }

    if build_style not in seconds_per_piece_map:
        raise ValueError("build_style must be 1 (slow), 2 (normal), or 3 (fast)")

    seconds_per_piece = seconds_per_piece_map[build_style]

    # --- Base time ---
    base_time_minutes = (piece_count * seconds_per_piece) / 60

    # --- Distraction multiplier ---
    if not (1 <= distraction_level <= 10):
        raise ValueError("distraction_level must be between 1 and 10")

    distraction_multiplier = 0.85 + (distraction_level - 1) * 0.05

    # --- Organization multiplier ---
    if not (1 <= organization_level <= 10):
        raise ValueError("organization_level must be between 1 and 10")

    organization_multiplier = 1.35 - (organization_level - 1) * 0.05

    # --- Difficulty multiplier ---
    difficulty_multiplier_map = {
        1: 0.95,
        2: 0.98,
        3: 1.00,
        4: 1.08,
        5: 1.15
    }

    if difficulty_level not in difficulty_multiplier_map:
        raise ValueError("difficulty_level must be between 1 and 5")

    difficulty_multiplier = difficulty_multiplier_map[difficulty_level]

    # --- Final estimated time ---
    estimated_minutes = (
        base_time_minutes
        * distraction_multiplier
        * organization_multiplier
        * difficulty_multiplier
    )

    return round(estimated_minutes, 1)