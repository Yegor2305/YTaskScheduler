$(document).ready(
    function(){
        $(document).on('change', '#group-select', function(){
            let groupId = $(this).val()
            $.ajax({
                url: '/groups_and_resources',
                method: 'GET',
                data: {
                    'action': 'group_changed',
                    'group_id': groupId
                },
                success: function(response) {
                    $('.groups-container').html(response)
                }
            })           
        })

        $(document).on('change', '#resource-select', function(){
            let resourceId = $(this).val()
            $.ajax({
                url: '/groups_and_resources',
                method: 'GET',
                data: {
                    'action': 'resource_changed',
                    'resource_id': resourceId
                },
                success: function(response) {
                    $('.resources-container').html(response)
                }
            })            
        })

        $(document).on('click', '#edit-group-button', function(){
            let groupId = $(this).data('group-id');
            $.ajax({
                url: '/groups_and_resources',
                method: 'GET',
                data: {
                    'action': 'edit_group',
                    'group_id': groupId
                },
                success: function(response) {
                    $('.groups-container').html(response)
                }
            })
        })

        $(document).on('click', '#edit-resource-button', function(){
            let resourceId = $(this).data('resource-id');
            $.ajax({
                url: '/groups_and_resources',
                method: 'GET',
                data: {
                    'action': 'edit_resource',
                    'resource_id': resourceId
                },
                success: function(response) {
                    $('.resources-container').html(response)
                }
            })
        })

        $(document).on('click', '.add-group-button', function(){
            $.ajax({
                url: '/groups_and_resources',
                method: 'GET',
                data: {
                    'action': 'add_group',
                },
                success: function(response) {
                    $('.groups-container').html(response)
                }
            })            
        })

        $(document).on('click', '.add-resource-button', function(){
            $.ajax({
                url: '/groups_and_resources',
                method: 'GET',
                data: {
                    'action': 'add_resource',
                },
                success: function(response) {
                    $('.resources-container').html(response)
                }
            })            
        })

        $(document).on('click', '#delete-group-button', function(){
            let groupId = $(this).data('group-id');
            if (confirm("Are you sure to delete group?")){
                $.ajax({
                    url: '/groups_and_resources',
                    method: 'GET',
                    data: {
                        'action': 'delete_group',
                        'group_id': groupId
                    },
                    success: function(response) {
                        $('.groups-container').html(response)
                    }
                }) 
            }                 
        })

        $(document).on('click', '#delete-resource-button', function(){
            let resourceId = $(this).data('resource-id');
            if (confirm("Are you sure to delete resource?")){
                $.ajax({
                    url: '/groups_and_resources',
                    method: 'GET',
                    data: {
                        'action': 'delete_resource',
                        'resource_id': resourceId
                    },
                    success: function(response) {
                        $('.resources-container').html(response)
                    }
                }) 
            }                 
        })
    }
)

function changeColor(){
    let color = $('#color-select').val();
    $('.group-info-color-content').css('background-color', color);
}