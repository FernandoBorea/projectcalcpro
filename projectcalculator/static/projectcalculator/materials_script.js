document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-material').forEach(element => {
        element.addEventListener('click', deleteMaterial);
    })
    document.querySelectorAll('.save-material').forEach(element => {
        element.addEventListener('click', saveMaterial);
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

    let material_id = this.dataset.materialId;
    let user_id = this.dataset.userId;
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
            /*
                Code to change status to saved and button to unsave.
                Use action to adjust this
            */
        })
}
