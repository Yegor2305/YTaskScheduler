$(document).ready(
    function(){
        $(document).on('change', '.change-task-state-checkbox', function(){
            let taskId = $(this).data('task-id');
            let taskState = this.checked;  
            console.log(taskState)
            $.ajax({
                url: '/tasks',
                method: 'GET',
                data: {
                    'action': 'change_task_state',
                    'task_id': taskId,
                    'task_state': taskState
                },
                success: function(response) {
                    $('.today-tasks-container').html(response)
                }
            })
                       
        })

        $(document).on('click', '.delete-task-button', function(){
            let taskId = $(this).data('task-id');
            if (confirm('Are you sure to delete task?')) {
                $.ajax({
                    url: '/tasks',
                    method: 'GET',
                    data: {
                        'action': 'delete',
                        'task_id': taskId
                    },
                    success: function(response) {
                        $('.today-tasks-container').html(response)
                    }
                })
            }           
        })

        $(document).on('click', '.task-field', function(){
            let taskId = $(this).data('task-id');
            $.ajax({
                url: '/tasks',
                method: 'GET',
                data: {
                    'action': 'show',
                    'task_id': taskId
                },
                success: function(response) {
                    $('.choosen-task-container').html(response)
                }
            })
        })
    }
)

document.querySelectorAll('.scrollable').forEach((element) => {
    const contentWidth = element.clientWidth
    const containerWidth = element.parentElement.clientWidth

    if (contentWidth > containerWidth){
        element.addEventListener('mouseenter', () => {
            element.classList.add('scroll')
        })

        element.addEventListener('mouseleave', () => {
            element.classList.remove('scroll')
        })
        
    }
})
