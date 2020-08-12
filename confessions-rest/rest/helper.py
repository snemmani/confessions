from rest_framework.response import Response
from rest_framework import status
from .models import Vote


def get_error_response(message, status):
    """Returns a Response object with specific error message and status code"""
    return Response(
        dict(error=message), status=status
    )


def get_response(response_dict, status=200):
    """Returns a Response object with specific response dict and status code
    Default status code is 200"""
    return Response(response_dict, status)


def do_vote(class_instance, object_id, request):
    # create filter criteria based on the class instance
    filter_criteria = {class_instance + '__id__exact': object_id}
    # Check if request has attribute vote_type in the body
    # if not, the raise bad request
    message = ''
    if 'vote_type' not in request.data:
        return get_error_response('Expected \'vote_type\' attibute in request body. Not found', status.HTTP_400_BAD_REQUEST)

    # Check if vote type is an integer with values +1 or -1 only
    if request.data['vote_type'] not in [1, -1]:
        return get_error_response('Only 1 and -1 values are supported for vote_type', status.HTTP_400_BAD_REQUEST)

    # Check if user already voted on the request
    votes = Vote.objects.filter(user__exact=request.user, **filter_criteria)
    if len(votes):
        vote = votes[0]
        # Check if the vote is similar, then remove the vote
        if vote.vote_type == request.data['vote_type']:
            vote.delete()
            message = 'Vote null as similar vote cast twice'
        else:
            # If yes, and the vote is vice versa, update
            vote.vote_type = vote.vote_type * -1
            message = 'Vote modified'

    else:
        # If no, then insert the vote
        insertion_object = {class_instance + '_id': object_id}
        Vote.objects.create(user=request.user, vote_type=request.data['vote_type'], **insertion_object)
        message = 'Vote inserted'

    return get_response(dict(message=message), status.HTTP_201_CREATED)
