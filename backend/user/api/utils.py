from rest_framework_simplejwt.tokens import RefreshToken

REFRESH = "refresh"
ACCESS = "access"
TOKEN = "token"
TOKEN_EXP_IN_SECONDS = "exp_time_seconds"


def get_tokens_for_user(user):
    refresh_token = RefreshToken.for_user(user)

    return {
        REFRESH: {
            TOKEN: str(refresh_token),
            TOKEN_EXP_IN_SECONDS: refresh_token.payload.get("exp"),
        },
        ACCESS: {
            TOKEN: str(refresh_token.access_token),
            TOKEN_EXP_IN_SECONDS: refresh_token.access_token.payload.get("exp"),
        },
    }


def get_refreshed_tokens(user):
    """ "Modify this to cater some refresh logic"""
    refresh = RefreshToken.for_user(user)

    return {
        REFRESH: str(refresh),
        ACCESS: str(refresh.access_token),
    }
