from django.shortcuts import get_object_or_404, render

from .serializers import UserSerializer
from .models import UserDetail
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import F
from django.utils import timezone 

rank_avi = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,8,8,4,2,2,1]
temp_rank_avi = {
    1:None, 
    2:None, 
    3:None, 
    4:None,
    5:None,
    6:None,
    7:None,
    8:None,
    9:None,
    10:None,
    11:None,
    12:8, 
    13:8,
    14:4,
    15:2, 
    16:2, 
    17:2
}


# utils to checck whether rank is full or not
def check_rank_avl(rank): 
    if rank>11 and rank<17:
        user1 = UserDetail.objects.filter(rank=rank)
        return user1.count()<rank_avi[rank]
    return True



# return all the memeber
@api_view(['GET'])
def list(request):
    queryset = UserDetail.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


# return a user detail
@api_view(['GET'])
def retrive(request,pk=None):
    queryset = UserDetail.objects.all()
    user = get_object_or_404(queryset,pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)



# Post to promote or demote user rank
@api_view(['POST'])
def update(request):
    task_val = {
        'promote':1, 
        'demote':-1
    }
    try:
        request_user = request.data["request_user"]
        base_user = request.data["base_user"]
        task = request.data["task"]

        user1 = UserDetail.objects.get(pk=request_user)
        user2 = UserDetail.objects.get(pk=base_user)

        if (task == 'promote' or task == 'demote') and user1.rank>14 and user1.rank>user2.rank:
            if check_rank_avl(user2.rank+task_val[task]): 
                user2.rank = user2.rank+task_val[task]
                user2.promoted_date = timezone.now()
                user2.xp = (2**(user2.rank-2))*1000
                user2.save()
                serializer = UserSerializer(user2)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else: 
                return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
        else: 
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response(status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)



# update user xp and rank if necessary
@api_view(['POST'])
def add_xp(request,pk):
    xp= request.data["xp"]
    user = UserDetail.objects.get(pk=pk)
    user.xp = F('xp') + xp
    user.save()
    user.refresh_from_db()
    if user.xp >= (2**(user.rank-1))*1000 and check_rank_avl(user.rank+1): 
        user.rank = F('rank') + 1
        user.promoted_date = timezone.now()
        user.save()
        user.refresh_from_db()
        serializer = UserSerializer(user)
        return Response({'new_rank':True,**serializer.data})
    return Response({'new_rank':False})


    

    
    # return Response(status=status.HTTP_400_BAD_REQUEST)


# add new user
@api_view(['POST'])
def create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# delete user
@api_view(['delete'])
def delete(request,id): 
    user = UserDetail.objects.get(id=id)
    user.delete()
    return Response(status=status.HTTP_200_OK)


# This function manages when someone left certain Post and promote the person who is queued for that rank
def manage_rank(): 
    pass

