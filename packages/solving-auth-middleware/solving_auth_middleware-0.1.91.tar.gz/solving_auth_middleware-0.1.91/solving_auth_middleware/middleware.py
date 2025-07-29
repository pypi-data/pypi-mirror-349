from flask import request, jsonify, current_app
from functools import wraps
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,

)

from flask_jwt_extended.exceptions import (
    JWTExtendedException,
    JWTDecodeError,
    InvalidHeaderError,
    InvalidQueryParamError,
    NoAuthorizationError,
    CSRFError,
    WrongTokenError,
    RevokedTokenError,
    FreshTokenRequired,
    UserLookupError,
    UserClaimsVerificationError
)
import requests
from typing import Optional, List, Callable

from solving_auth_middleware.enums import UserTypeEnum

def verify_permissions_from_api(identity: str, endpoint: str, token: str, permissions: List[str]) -> bool:
    """Vérifie les permissions auprès de l'API de permissions."""
    try:
        response = requests.post(
            endpoint,
            json={'identity': identity, 'permissions': permissions},
            headers={'Authorization': f'Bearer {token}'},
            timeout=current_app.config['PERMISSIONS_API_TIMEOUT']
        )
        return response.status_code == 200
    except requests.RequestException:
        return False

def verify_permissions_from_function(identity: str, function: Callable, permissions: List[str]) -> bool:
    """Vérifie les permissions auprès de la fonction."""
    return function(identity, permissions)

def requires_permissions(
    user_type: UserTypeEnum = UserTypeEnum.PRO,
    location: str = 'header',
    fresh: bool = False,
    audit_fn: Optional[Callable] = None,
    verify_fn: Optional[Callable] = None,
    required_permissions: Optional[List[str]] = None,
):
    """
    Décorateur pour vérifier les permissions.
    Utilise jwt_required en interne pour la validation du JWT.
    
    Args:
        user_type.value: Type d'utilisateur ('public', 'pro', 'side_admin')
        location: Emplacement du token ('header', 'cookies', 'query_string', 'json')
        fresh: Si True, exige un token frais
        audit_fn: Fonction optionnelle pour l'audit
        verify_fn: Fonction personnalisée pour la vérification des permissions
        required_permissions: Liste des permissions requises (utilisé avec verify_fn)
        jwt_manager: Instance optionnelle de JWTManager à utiliser
    """
    def wrapper(fn):
        @wraps(fn)
        @jwt_required(locations=[location], fresh=fresh)
        def decorator(*args, **kwargs):
            try:
                # Récupération des informations du JWT
                jwt_data = get_jwt()
                identity = get_jwt_identity()
                token = request.headers.get('Authorization', '').split(' ')[1]

                # Vérification des permissions
                if verify_fn is not None:
                    # Vérification via fonction personnalisée
                    if not verify_permissions_from_function(identity, verify_fn, required_permissions or []):
                        return jsonify({"msg": f"Insufficient permissions for {user_type.value} user"}), 403
                else:
                    # Vérification via API
                    endpoint = current_app.config.get(f'{user_type.value.upper()}_USER_API_ENDPOINT')
                    if not endpoint:
                        return jsonify({"msg": f"Invalid user type: {user_type.value}"}), 400
                    if not verify_permissions_from_api(identity, endpoint, token, required_permissions or []):
                        return jsonify({"msg": f"Insufficient permissions for {user_type.value} user"}), 403

                # Audit si nécessaire
                if audit_fn:
                    audit_fn(identity, request)
            except NoAuthorizationError as e:
                return jsonify({"msg": "Missing authorization token", "error": str(e)}), 401
            except JWTDecodeError as e:
                return jsonify({"msg": "Invalid token format", "error": str(e)}), 401
            except InvalidHeaderError as e:
                return jsonify({"msg": "Invalid authorization header", "error": str(e)}), 401
            except InvalidQueryParamError as e:
                return jsonify({"msg": "Invalid token in query parameters", "error": str(e)}), 401
            except CSRFError as e:
                return jsonify({"msg": "CSRF protection failed", "error": str(e)}), 401
            except WrongTokenError as e:
                return jsonify({"msg": "Wrong token type used", "error": str(e)}), 401
            except RevokedTokenError as e:
                return jsonify({"msg": "Token has been revoked", "error": str(e)}), 401
            except FreshTokenRequired as e:
                return jsonify({"msg": "Fresh token required", "error": str(e)}), 401
            except UserLookupError as e:
                return jsonify({"msg": "User not found", "error": str(e)}), 401
            except UserClaimsVerificationError as e:
                return jsonify({"msg": "Invalid user claims", "error": str(e)}), 401
            except requests.RequestException as e:
                return jsonify({"msg": "Permission service unavailable", "error": str(e)}), 503
            except Exception as e: 
                ## TODO : Raise les 401 et les 401 
                return jsonify({"msg": "Permission verification failed", "error": str(e)}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper