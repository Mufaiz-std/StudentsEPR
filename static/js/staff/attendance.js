document.addEventListener('DOMContentLoaded', () => {
    const saveBtn = document.getElementById('save-attendance-btn');
    const attendanceApp = document.getElementById('attendance-app');
    if (!saveBtn || !attendanceApp) return;

    const submitUrl = attendanceApp.dataset.submitUrl;

    saveBtn.addEventListener('click', async () => {
        const subjectId = document.getElementById('subject-select').value;
        const attendanceDate = document.getElementById('attendance-date').value;
        const presentStudentIds = Array.from(document.querySelectorAll('.student-checkbox:checked')).map(
            checkbox => checkbox.value
        );

        if (!attendanceDate) {
            alert('Please select a date.');
            return;
        }

        const payload = {
            subject_id: subjectId,
            attendance_date: attendanceDate,
            student_ids: presentStudentIds,
        };

        try {
            const response = await fetch(submitUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify(payload),
            });

            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Request failed', error);
            alert('Unable to save attendance. Please try again.');
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === `${name}=`) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
