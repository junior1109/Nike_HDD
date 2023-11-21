function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

  var bouncingShoes = anime({
    targets: '#shoe-target',
    translateY: '15',
    duration: 2000,
    loop: true,
    direction: 'alternate',
    easing: 'linear'
  });