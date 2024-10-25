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
                    $('.task-container').html(response)
                }
            })
        })

        $(document).on('click', '.add-task-button', function(){
            $.ajax({
                url: '/tasks',
                method: 'GET',
                data: {
                    'action': 'add_task',
                },
                success: function(response) {
                    $('.task-container').html(response);
                }
            })
        })

        $(document).on('click', '.edit-task-button', function(){
            let taskId = $(this).data('task-id');
            $.ajax({
                url: '/tasks',
                method: 'GET',
                data: {
                    'action': 'edit_task',
                    'task_id': taskId
                },
                success: function(response) {
                    $('.task-container').html(response);
                }
            })
        })
    }
)



function addResourceForTask(){
    let resourceSelect = $('#resource-select').val();
    let resourceCount = $('#resource-count').val();
    if (resourceSelect == "None") { return }
    $.ajax({
        url: '/tasks',
        method: 'GET',
        data: {
            'action': 'add_resource_for_task',
            'resource_id': resourceSelect,
            'resource_count': resourceCount
        },
        success: function(response) {
            $('.task-info-resources-content').text(response.resources_label);
        }
    })
}

function removeResourceFromTask(){
    let resourceSelect = $('#resource-select').val();
    if (resourceSelect == "None") { return }
    $.ajax({
        url: '/tasks',
        method: 'GET',
        data: {
            'action': 'remove_resource_from_task',
            'resource_id': resourceSelect,
        },
        success: function(response) {
            $('.task-info-resources-content').text(response.resources_label);
        }
    })
}

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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});