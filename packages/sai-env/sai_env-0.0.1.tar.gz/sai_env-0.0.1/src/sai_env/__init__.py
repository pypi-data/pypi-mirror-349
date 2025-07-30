from gymnasium import register

register(
    id="GolfCourseEnv-v0",
    entry_point="sai_env.golf_course_env:GolfCourseEnv",
)