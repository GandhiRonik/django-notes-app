from django.shortcuts import render
from django.http import JsonResponse          # NEW IMPORT — needed for health response
from django.db import connection              # NEW IMPORT — needed to test DB connectivity
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import Note


# ─── NEW: Health Check View ────────────────────────────────────────────────────
# This view does NOT use @api_view because:
# 1. It must respond even if DRF has an issue
# 2. JsonResponse is lighter and more appropriate for infra health checks
# 3. Jenkins/load balancers don't need DRF's content negotiation
def health_check(request):
    """
    Returns 200 JSON if the app AND database are healthy.
    Returns 503 JSON if the database connection fails.
    Used by the Jenkins pipeline to verify deployments before marking them successful.
    """
    try:
        # This actually opens a real connection to the DB and pings it.
        # If the DB is down, misconfigured, or credentials are wrong,
        # this line will raise an exception and we catch it below.
        connection.ensure_connection()
        db_status = "healthy"
    except Exception as e:
        # Return 503 Service Unavailable — Jenkins treats any non-200 as failure
        return JsonResponse(
            {
                "status": "unhealthy",
                "db": "unreachable",
                "error": str(e),
            },
            status=503,
        )

    # Both app and DB are fine — return 200
    return JsonResponse(
        {
            "status": "healthy",
            "db": db_status,
        },
        status=200,
    )
# ──────────────────────────────────────────────────────────────────────────────


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]
    return Response(routes)


@api_view(['GET'])
def getNotes(request):
    notes = Note.objects.all().order_by('-created')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getNote(request, pk):
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def updateNote(request, pk):
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(instance=note, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteNote(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return Response('Note was deleted!')


@api_view(['POST'])
def createNote(request):
    data = request.data
    note = Note.objects.create(
        body=data['body']
    )
    serializer = NoteSerializer(note, many=False)
