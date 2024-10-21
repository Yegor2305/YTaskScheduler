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

        $('.show-task-button').click(function(){
            let taskId = $(this).data('task-id');
            $.ajax({
                url: '/tasks',
                method: 'GET',
                data: {
                    'action': 'show',
                    'task_id': taskId
                },
                success: function(response) {
                    $('body').html(response);
                }
            })
        })
    }
)

document.querySelectorAll('.task-name-content').forEach((element) => {
        const contentWidth = element.clientWidth
        const taskNameWidth = document.querySelector('.task-name').clientWidth

        if (contentWidth > taskNameWidth){
            element.addEventListener('mouseenter', () => {
                element.classList.add('scroll')
            })

            element.addEventListener('mouseleave', () => {
                element.classList.remove('scroll')
            })
            
        }
        // element.addEventListener('mouseenter', () =>{
        //     const contentWidth = element.scrollWidth
        //     const visibleWidth = element.clientWidth

        //     if (contentWidth > visibleWidth){
        //         element.style.transform = `translateX(-${visibleWidth - contentWidth}px)`;
        //         console.log(element.style.transform)
        //     }   
        // })
    })
