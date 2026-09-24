from hypothesis import HealthCheck, settings

# Global profile so Hypothesis doesn't fail due to mutmut's isolated/parallel executors
settings.register_profile(
    "mutmut_profile",
    suppress_health_check=[HealthCheck.differing_executors]
)

# Load profile automatically
settings.load_profile("mutmut_profile")
