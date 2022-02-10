from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from api.family_datastructure import Family
import json
from functools import reduce

# initialize a 'Doe' family
family = Family(last_name='Doe')

"""
The MembersView will contain the logic on how to:
 GET, POST, PUT or delete family members
"""
class MembersView(APIView):
    def get(self, request, member_id=None):
        members = family.get_all_members()
        i = 0
        all_lucky_numbers = []
        while i < len(members):
            all_lucky_numbers = all_lucky_numbers + members[i]["lucky_numbers"]
            i += 1
        if member_id == None:
            result = {
                "members": members,
                "family_name": family.last_name,
                "lucky_numbers": all_lucky_numbers,
                "sum_of_lucky": reduce(lambda x, y : x + y, all_lucky_numbers)
                }
        else:
            result = family.get_member(member_id)
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        member = json.loads(request.body)
        family.add_member(member)
        result = "ok"
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, member_id=None):
        member = json.loads(request.body)
        family.update_member(member_id, member)
        result = "ok"
        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request, member_id=None):
        family.delete_member(member_id)
        return Response({ "status": "ok" }, status=status.HTTP_200_OK)