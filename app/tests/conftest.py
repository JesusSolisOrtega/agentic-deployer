from hypothesis import HealthCheck, settings

# Perfil global para que Hypothesis no falle por los executors paralelos/aislados de mutmut
settings.register_profile(
    "mutmut_profile",
    suppress_health_check=[HealthCheck.differing_executors]
)

# Cargar el perfil automáticamente
settings.load_profile("mutmut_profile")
