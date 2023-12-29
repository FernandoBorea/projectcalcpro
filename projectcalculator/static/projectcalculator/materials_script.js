const save_material_listener = function() {saveMaterial()};
const unsave_material_listener = function() {saveMaterial(unsave = true)};

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-material').forEach(element => {
        element.addEventListener('click', deleteMaterial);
    })
    document.querySelectorAll('.save-material').forEach(element => {
        element.addEventListener('click', save_material_listener);
    })
    document.querySelectorAll('.unsave-material').forEach(element => {
        element.addEventListener('click', unsave_material_listener);
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

function deleteMaterial() {

    let material_id = this.dataset.materialId;
    let csrf_token = getCookie('csrftoken');

    fetch('/delete_material', {
        method: 'DELETE',
        headers: {'X-CSRFToken': csrf_token},
        mode: 'same-origin',
        body: JSON.stringify({
            'material_id': material_id,
        })
    })
    .then(response => response.json())
    .then(data => {
        let material_container = document.querySelector(`.material-${material_id}-container`);
        material_container.remove();
        console.log(`Completed deletion of material ${material_id} with response: ${data}`);
    })
}

function saveMaterial(unsave = false) {

    let button = event.target;
    let material_id = button.dataset.materialId;
    let user_id = button.dataset.userId;
    let action = (!unsave)? 0 : 1;
    let csrf_token = getCookie('csrftoken');

        fetch('/save_material', {
            method: 'PUT',
            headers: {'X-CSRFToken': csrf_token},
            body: JSON.stringify({
                'action': action,
                'material_id': material_id,
                'user_id': user_id
            })
        })
        .then(response => response.json())
        .then(data => {
            if (action == 0) {
                button.className = "btn btn-outline-primary unsave-material";
                button.innerHTML = "Unsave";
                button.removeEventListener('click', save_material_listener);
                button.addEventListener('click', unsave_material_listener);
            } else {
                button.className = "btn btn-outline-primary save-material";
                button.innerHTML = "Save";
                button.removeEventListener('click', unsave_material_listener);
                button.addEventListener('click', save_material_listener);
            }
        })
}
