import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import createUser, validateFieldsPassed, skip_firebase_auth
from .responses import create_response
import json
from .models import Role, CustomUser, Organisation
from firebase_admin import auth
from django.forms.models import model_to_dict
from .serializer import CustomUserSerializer, OrganisationsSerializer


logger = logging.getLogger(__name__)

# Create your views here.
@csrf_exempt
def my_view(request):
    user = getattr(request, 'firebase_user', None)
    return create_response(404, "Success", {'message': f'Hello {user.username}'})

@csrf_exempt
@skip_firebase_auth
def createNewUser(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if not auth_header.startswith("Bearer "):
        return create_response(401, "unauthorised", "Bad Request")
    id_token = auth_header.split("Bearer ")[-1]
    try:
        body_str = request.body.decode('utf-8')
        data = json.loads(request.body)
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        print(uid)
        result = validateFieldsPassed(data, "username", "firstName", "lastName", "phoneNumber")
        if result is not None:
            return create_response(502, "bad request", "Expected fields " + result)

        client_role = Role.objects.get(name="client")
        user = CustomUser(
            firebase_uid = uid,
            first_name = data.get("firstName"),
            last_name = data.get("lastName")
        )
        user.save()
        user.roles.set([client_role])
        user.save()
        return create_response(502, "bad request", model_to_dict(user))
    except Exception as e:
        logger.exception("Something went wrong: %s", e)
        return create_response(502, "bad request", str(e))

@csrf_exempt
def createOrganisation(request):
    body_str = request.body.decode('utf-8')
    data = json.loads(request.body)
    result = validateFieldsPassed(data, "name", "primaryPhoneNumber")
    if result is not None:
        return create_response(502, "bad request", "Expected fields " + result)

    user = request.firebase_user
    organisation = Organisation(
        name = data.get("name"),
        primaryPhoneNumber = data.get("primaryPhoneNumber"),
        admin = user
    )
    organisation.save()

    admin_role = Role.objects.get(name="admin")
    user.roles.set([admin_role])
    user.organisation = organisation
    user.save()
    res = OrganisationsSerializer(instance=organisation)
    return create_response(200, "success", res.data)

@csrf_exempt
def getUserDetails(request):
    res = CustomUserSerializer(instance=request.firebase_user)
    return create_response(200, "success", res.data)

@csrf_exempt
def getOrganisationDetails(request):
    res = OrganisationsSerializer(instance=request.firebase_user.organisation)
    return create_response(200, "success", res.data)
