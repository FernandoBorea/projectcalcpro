document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-project').forEach(element => {
        element.addEventListener('click', deleteProject);
    })
    document.querySelectorAll('.save-project').forEach(element => {
        element.addEventListener('click', saveProject);
    })
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function deleteProject() {

    let project_id = this.dataset.projectId;
    let csrf_token = getCookie('csrftoken');

    fetch('/delete_project', {
        method: 'DELETE',
        headers: {'X-CSRFToken': csrf_token},
        mode: 'same-origin',
        body: JSON.stringify({
            'project_id': project_id,
        })
    })
    .then(response => response.json())
    .then(data => {
        let project_container = document.querySelector(`.project-${project_id}-container`);
        project_container.remove();
        console.log(`Completed deletion of material ${project_id} with response: ${data}`);
    })
}

function saveProject(unsave = false) {

    let project_id = this.dataset.projectId;
    let user_id = this.dataset.userId;
    let action = (!unsave)? 0 : 1;
    let csrf_token = getCookie('csrftoken');

        fetch('/save_project', {
            method: 'PUT',
            headers: {'X-CSRFToken': csrf_token},
            body: JSON.stringify({
                'action': action,
                'project_id': project_id,
                'user_id': user_id
            })
        })
        .then(response => response.json())
        .then(data => {
            /*
                Code to change status to saved and button to unsave.
                Use action to adjust this
            */
        })
}