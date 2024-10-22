$(document).ready(
    function(){
        $('.delete-task-button').click(function(){
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
                        location.reload();
                    }
                })
            }           
        })

        $('.task-field').click(function(){
            let taskId = $(this).data('task-id');
            $.ajax({
                url: '/tasks',
                method: 'GET',
                data: {
                    'action': 'show',
                    'task_id': taskId
                },
                success: function(response) {
                    $('#choosen-task-name').text(response.name)
                    $('.choosen-task-description-content').text(response.description)
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
