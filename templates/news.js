const Like = document.getElementById('Like');
const Dislike = document.getElementById('Dislike');

Like.addEventListener('click', function onClick() {
  btn.style.backgroundColor = 'green';
  btn.style.color = 'white';
});


Dislike.addEventListener('click', function onClick() {
  btn.style.backgroundColor = 'red';
  btn.style.color = 'white';
});
