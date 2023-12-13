document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-material').forEach(element => {
        element.addEventListener('click', deleteMaterial)
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

function saveProject(unsave = false) {

    let material_id = this.dataset.materialId;

    if (!unsave)
    {
        fetch('/save_project', {
            method: 'PUT',
            body: JSON.stringify({
                'action': 0,
                'material_id': material_id
            })
        })
        .then(response => response.json())
        .then(data => {
            /*
                Code to change status to saved and button to unsave
            */
        })

        return;
    }

    fetch('/save_project', {
        method: 'PUT',
        body: JSON.stringify({
            'action': 1,
            'material_id': material_id
        })
    })
    .then(response => response.json())
    .then(data => {
        /*
            Code to change the status to unsaved and button to save
        */
    })
}
