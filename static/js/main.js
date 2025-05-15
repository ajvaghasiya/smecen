document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle
    const sidebar = document.querySelector('.sidebar');
    const sidebarBtn = document.querySelector('.sidebarBtn');
    
    sidebarBtn.addEventListener('click', () => {
        sidebar.classList.toggle('close');
    });

    // Mobile Responsive Sidebar
    function checkWidth() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('close');
        } else {
            sidebar.classList.remove('close');
        }
    }

    window.addEventListener('resize', checkWidth);
    checkWidth();

    // Notifications Dropdown
    const notificationBtn = document.querySelector('.notification');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', () => {
            // Add your notification dropdown logic here
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // DataTables initialization
    const tables = document.querySelectorAll('.datatable');
    tables.forEach(table => {
        if (typeof $.fn.DataTable !== 'undefined') {
            $(table).DataTable({
                responsive: true,
                pageLength: 10,
                language: {
                    search: "",
                    searchPlaceholder: "Search..."
                }
            });
        }
    });

    // Chart.js initialization
    const chartElements = document.querySelectorAll('.chart');
    chartElements.forEach(element => {
        const type = element.dataset.type || 'line';
        const data = JSON.parse(element.dataset.data || '{}');
        
        new Chart(element, {
            type: type,
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    });
}); 