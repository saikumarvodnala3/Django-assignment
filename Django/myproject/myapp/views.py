from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Issue, Agents, Mechanic

@csrf_exempt
def create_issue(request):
    if request.method == 'POST':
        # Extract data from the request
        data = {
            'userID': request.POST.get('userID'),
            'location': request.POST.get('location'),
            'problem': request.POST.get('problem'),
        }
        
        # Create a new issue
        issue = Issue.objects.create(**data)
        
        # Randomly assign an agent with the least requests in their queue
        agents = Agents.objects.order_by('queue')
        assigned_agent = agents.first()
        assigned_agent.queue += 1
        assigned_agent.save()
        
        # Update issue status
        issue.status = 'ASSIGNED'
        issue.save()
        
        return JsonResponse({'message': 'Issue created successfully'})
    return JsonResponse({'message': 'Invalid request method'})
@csrf_exempt
def get_issues(request):
    if request.method == 'GET':
        # Get a list of all issues
        issues = Issue.objects.all()
        
        # Serialize the issues and return as JSON response
        serialized_issues = [{'issueID': issue.issueID, 'userID': issue.userID, 'location': issue.location, 'problem': issue.problem, 'time': issue.time, 'status': issue.status} for issue in issues]
        
        return JsonResponse(serialized_issues, safe=False)

@csrf_exempt
def get_issue_details(request, issueID):
    if request.method == 'GET':
        try:
            # Get details of a specific issue
            issue = Issue.objects.get(issueID=issueID)
            
            # Serialize the issue and return as JSON response
            serialized_issue = {'issueID': issue.issueID, 'userID': issue.userID, 'location': issue.location, 'problem': issue.problem, 'time': issue.time, 'status': issue.status}
            
            return JsonResponse(serialized_issue)
        except Issue.DoesNotExist:
            return JsonResponse({'error': 'Issue not found'}, status=404)

@csrf_exempt
def get_agents(request):
    if request.method == 'GET':
        # Get a list of all agents
        agents = Agents.objects.all()
        
        # Serialize the agents and return as JSON response
        serialized_agents = [{'agentID': agent.agentID, 'queue': agent.queue} for agent in agents]
        
        return JsonResponse(serialized_agents, safe=False)

@csrf_exempt
def get_mechanics(request):
    if request.method == 'GET':
        # Get a list of all mechanics
        mechanics = Mechanic.objects.all()
        
        # Serialize the mechanics and return as JSON response
        serialized_mechanics = [{'mechanicID': mechanic.mechanicID, 'availability': mechanic.availability} for mechanic in mechanics]
        
        return JsonResponse(serialized_mechanics, safe=False)
