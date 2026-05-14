document.addEventListener('DOMContentLoaded', () => {
    const saveBtn = document.getElementById('save-staff-attendance-btn');
    const app = document.getElementById('staff-attendance-app');
    if (!saveBtn || !app) return;

    const submitUrl = app.dataset.submitUrl;
    saveBtn.addEventListener('click', async () => {
        const attendanceDate = document.getElementById('attendance-date').value;
        const staffIds = Array.from(document.querySelectorAll('.staff-checkbox:checked')).map(
            checkbox => checkbox.value
        );

        if (!attendanceDate) {
            alert('Please select the attendance date.');
            return;
        }

        try {
            const response = await fetch(submitUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    attendance_date: attendanceDate,
                    staff_ids: staffIds,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Save failed', error);
            alert('Unable to save attendance. Please try again.');
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const trimmed = cookie.trim();
                if (trimmed.startsWith(`${name}=`)) {
                    cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
