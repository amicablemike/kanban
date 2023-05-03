from kanban.base.models import Task, Board


Task.objects.all().delete()
Board.objects.all().delete()

print('success')