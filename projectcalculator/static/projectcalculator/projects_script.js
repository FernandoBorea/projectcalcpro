const save_project_listener = function() {saveProject()};
const unsave_project_listener = function() {saveProject(unsave = true)};

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-project').forEach(element => {
        element.addEventListener('click', deleteProject);
    })
    document.querySelectorAll('.save-project').forEach(element => {
        element.addEventListener('click', save_project_listener);
    })
    document.querySelectorAll('.unsave-project').forEach(element => {
        element.addEventListener('click', unsave_project_listener);
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

    let button = event.target;
    let project_id = button.dataset.projectId;
    let user_id = button.dataset.userId;
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
            if (action == 0) {
                button.className = "mt-3 btn btn-outline-primary unsave-project";
                button.innerHTML = "Unsave";
                button.removeEventListener('click', save_project_listener);
                button.addEventListener('click', unsave_project_listener);
            } else {
                button.className = "mt-3 btn btn-outline-primary save-project";
                button.innerHTML = "Save";
                button.removeEventListener('click', unsave_project_listener);
                button.addEventListener('click', save_project_listener);
            }
        })
}