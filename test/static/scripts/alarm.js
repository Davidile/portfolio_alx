document.addEventListener('DOMContentLoaded', function () {
    const messages = document.querySelectorAll('.btn-success, .btn-danger');
    messages.forEach(function (element) {
       element.style.display = 'block';
       setTimeout(function () {
          element.style.display = 'none';
       }, 1000);  
    });
 });
 