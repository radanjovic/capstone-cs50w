/* Dynamic(as you type search of Users who are also authors) */
/* Code by: SHxKM from GitHub, repository: django-ajax-search */
const user_input = $("#user-input")
const search_icon = $('#search-icon')
const artists_div = $('#replaceable-content')
const endpoint = '/writerhub/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
	$.getJSON(endpoint, request_parameters)
		.done(response => {
			// fade out the artists_div, then:
			artists_div.fadeTo('slow', 0).promise().then(() => {
				// replace the HTML contents
				artists_div.html(response['html_from_view'])
				// fade-in the div with new contents
				artists_div.fadeTo('slow', 1)
				// stop animating search icon
				search_icon.removeClass('blink')
			})
		})
}

user_input.on('keyup', function () {

	const request_parameters = {
		q: $(this).val() // value of user_input: the HTML element with ID user-input
	}

	// start animating the search icon with the CSS class
	search_icon.addClass('blink')

	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})

/* MyProfile one page app - changing the views on clicks. */
document.addEventListener('DOMContentLoaded', function() {
	document.querySelector('#mp_scripts').addEventListener('click', scripts_view);
	document.querySelector('#mp_reading').addEventListener('click', reading_view);
	document.querySelector('#mp_read_later').addEventListener('click', read_later_view);
	document.querySelector('#mp_favorite').addEventListener('click', favorite_view);
	document.querySelector('#mp_notes').addEventListener('click', notes_view);

	/* Default view */
	document.querySelector("#mp_scripts_view").style.display = 'block';
	document.querySelector("#mp_reading_view").style.display = 'none';
	document.querySelector("#mp_read_later_view").style.display = 'none';
	document.querySelector("#mp_favorite_view").style.display = 'none';
	document.querySelector("#mp_notes_view").style.display = 'none';
});
function scripts_view() {
	document.querySelector("#mp_scripts_view").style.display = 'block';
	document.querySelector("#mp_reading_view").style.display = 'none';
	document.querySelector("#mp_read_later_view").style.display = 'none';
	document.querySelector("#mp_favorite_view").style.display = 'none';
	document.querySelector("#mp_notes_view").style.display = 'none';
};
function reading_view() {
	document.querySelector("#mp_scripts_view").style.display = 'none';
	document.querySelector("#mp_reading_view").style.display = 'block';
	document.querySelector("#mp_read_later_view").style.display = 'none';
	document.querySelector("#mp_favorite_view").style.display = 'none';
	document.querySelector("#mp_notes_view").style.display = 'none';
};
function read_later_view() {
	document.querySelector("#mp_scripts_view").style.display = 'none';
	document.querySelector("#mp_reading_view").style.display = 'none';
	document.querySelector("#mp_read_later_view").style.display = 'block';
	document.querySelector("#mp_favorite_view").style.display = 'none';
	document.querySelector("#mp_notes_view").style.display = 'none';
};
function favorite_view() {
	document.querySelector("#mp_scripts_view").style.display = 'none';
	document.querySelector("#mp_reading_view").style.display = 'none';
	document.querySelector("#mp_read_later_view").style.display = 'none';
	document.querySelector("#mp_favorite_view").style.display = 'block';
	document.querySelector("#mp_notes_view").style.display = 'none';
};
function notes_view() {
	document.querySelector("#mp_scripts_view").style.display = 'none';
	document.querySelector("#mp_reading_view").style.display = 'none';
	document.querySelector("#mp_read_later_view").style.display = 'none';
	document.querySelector("#mp_favorite_view").style.display = 'none';
	document.querySelector("#mp_notes_view").style.display = 'block';
};

/* Read view - changing fonts, bcgr and text colors, and font sizes on user input */
document.addEventListener('DOMContentLoaded', function() {
	document.querySelector('#read_arial').addEventListener('click', read_arial);
	document.querySelector('#read_courier').addEventListener('click', read_courier);
	document.querySelector('#read_georgia').addEventListener('click', read_georgia);
	document.querySelector('#read_times').addEventListener('click', read_times);
	document.querySelector('#read_verdana').addEventListener('click', read_verdana);

	document.querySelector('#read_white').addEventListener('click', read_white);
	document.querySelector('#read_sandpaper').addEventListener('click', read_sandpaper);
	document.querySelector('#read_grey').addEventListener('click', read_grey);
	document.querySelector('#read_black').addEventListener('click', read_black);

	document.querySelector('#read_small').addEventListener('click', read_small);
	document.querySelector('#read_medium').addEventListener('click', read_medium);
	document.querySelector('#read_large').addEventListener('click', read_large);
});
function read_arial() {
	document.querySelector('#readContent').style.fontFamily = 'Arial, Helvetica, sans-serif';
};
function read_courier() {
	document.querySelector('#readContent').style.fontFamily = "'Courier New', Courier, monospace";
};
function read_georgia() {
	document.querySelector('#readContent').style.fontFamily = 'Georgia, Times, serif';
};
function read_times() {
	document.querySelector('#readContent').style.fontFamily = "'Times New Roman', Times, serif";
};
function read_verdana() {
	document.querySelector('#readContent').style.fontFamily = 'Verdana, Tahoma, sans-serif';
};
function read_white() {
	document.querySelector('#readContent').style.backgroundColor = 'white';
	document.querySelector('#readContent').style.color = 'black';
	document.querySelector('#readContent').style.borderColor = 'black';
};
function read_sandpaper() {
	document.querySelector('#readContent').style.backgroundColor = 'blanchedAlmond';
	document.querySelector('#readContent').style.color = 'black';
	document.querySelector('#readContent').style.borderColor = 'black';
};
function read_grey() {
	document.querySelector('#readContent').style.backgroundColor = 'dimGray';
	document.querySelector('#readContent').style.color = 'white';
	document.querySelector('#readContent').style.borderColor = 'white';
};
function read_black() {
	document.querySelector('#readContent').style.backgroundColor = 'black';
	document.querySelector('#readContent').style.color = 'white';
	document.querySelector('#readContent').style.borderColor = 'white';
};
function read_small() {
	document.querySelector('#readContent').style.fontSize = 'small';
};
function read_medium() {
	document.querySelector('#readContent').style.fontSize = 'medium';
};
function read_large() {
	document.querySelector('#readContent').style.fontSize = 'larger';
};

/* Read view - dynamically adding Save Note button after selection of text */
document.addEventListener('DOMContentLoaded', function() {
	/* Use this functions only in a div that contains displayed contents of files */
	const content = document.querySelector('#docContent');
	/* Create and append button for saving the note */
	const noteBtn = document.createElement('button');
	noteBtn.innerHTML = 'Save Note';
	noteBtn.style.position = 'absolute';
	noteBtn.style.display = 'none';
	noteBtn.className = 'btn btn-sm btn-danger';

	content.appendChild(noteBtn);

	let startX = 0;
	let startY = 0;

	/* On mousedown only save starting X and Y, but relevant to entire page, 
	 not the client X and Y, which causes button to stay on top part of doc,
	 even if we want to select text from bottom part. */
	content.addEventListener('mousedown', function(evt){
		startX = evt.pageX;
		startY = evt.pageY;
	});
	
	/* On mouse up, we check if the end X and Y differ from starting
	and if, we place the button to the end of the selection, where user's
	mouse will naturally be, after making the selection. 
	If the start and end X and Y do not differ, most likely user wanted to 
	click somewhere to 'hide' the popped up button, so we just set its display
	 to none in such case*/
	content.addEventListener('mouseup', function(evt) {  
		if (evt.pageX != startX && evt.pageY != startY ) {
			noteBtn.style.top = `${evt.pageY}px`;
			noteBtn.style.left = `${evt.pageX}px`;
			noteBtn.style.display = 'block';
		} else {
			noteBtn.style.display = 'none';
		}
	});

	/* Finally, we add event listener for clicks on button, and when the button is
	clicked we save the text to const, and pass that to our view */
	noteBtn.addEventListener('click', function() {
		const note = document.getSelection().toString();
		const id = content.querySelector('.reading_content_id').value;
		fetch(`/add_note/${id}`, {
			method: 'POST',
			body: JSON.stringify({
				note:`${note}`
			})
		}).then (function() {
			document.getSelection().collapseToEnd();
			noteBtn.style.display = 'none';
		});
	});
});


/* Deleting selected note */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#mp_notes_view').addEventListener('click', function(e) {
        const tgt = e.target.closest('.delete_note');
        if (tgt) {
			const noteDiv = tgt.closest('.mp_notes_container');
            const id = noteDiv.querySelector('.note_id').value; 
            fetch(`/delete_note/${id}`, {
                method: 'POST',
                body: JSON.stringify({
                  action: 'delete'
                })
              }).then (function() {
                    noteDiv.style.display = 'none';
              });
        }
    });
});

/* Changing the color of rating stars based on avg rate */
document.addEventListener('DOMContentLoaded', function() {
	const slDiv = document.querySelector('#storyline_rating');
	const slAvg = document.querySelector('#sl_avg_r').value;
	if (slAvg >= 4.5) {
		slDiv.querySelector('#sl2').classList.add('checked');
		slDiv.querySelector('#sl3').classList.add('checked');
		slDiv.querySelector('#sl4').classList.add('checked');
		slDiv.querySelector('#sl5').classList.add('checked');
	} else if (slAvg >= 3.5) {
		slDiv.querySelector('#sl2').classList.add('checked');
		slDiv.querySelector('#sl3').classList.add('checked');
		slDiv.querySelector('#sl4').classList.add('checked');
	} else if (slAvg >= 2.5) {
		slDiv.querySelector('#sl2').classList.add('checked');
		slDiv.querySelector('#sl3').classList.add('checked');
	} else if (slAvg >= 1.5) {
		slDiv.querySelector('#sl2').classList.add('checked');
	}

	const chDiv = document.querySelector('#characters_rating');
	const chAvg = document.querySelector('#ch_avg_r').value;
	if (chAvg >= 4.5) {
		chDiv.querySelector('#ch2').classList.add('checked');
		chDiv.querySelector('#ch3').classList.add('checked');
		chDiv.querySelector('#ch4').classList.add('checked');
		chDiv.querySelector('#ch5').classList.add('checked');
	} else if (chAvg >= 3.5) {
		chDiv.querySelector('#ch2').classList.add('checked');
		chDiv.querySelector('#ch3').classList.add('checked');
		chDiv.querySelector('#ch4').classList.add('checked');
	} else if (chAvg >= 2.5) {
		chDiv.querySelector('#ch2').classList.add('checked');
		chDiv.querySelector('#ch3').classList.add('checked');
	} else if (chAvg >= 1.5) {
		chDiv.querySelector('#ch2').classList.add('checked');
	}

	const wrDiv = document.querySelector('#writing_rating');
	const wrAvg = document.querySelector('#wr_avg_r').value;
	if (wrAvg >= 4.5) {
		wrDiv.querySelector('#wr2').classList.add('checked');
		wrDiv.querySelector('#wr3').classList.add('checked');
		wrDiv.querySelector('#wr4').classList.add('checked');
		wrDiv.querySelector('#wr5').classList.add('checked');
	} else if (wrAvg >= 3.5) {
		wrDiv.querySelector('#wr2').classList.add('checked');
		wrDiv.querySelector('#wr3').classList.add('checked');
		wrDiv.querySelector('#wr4').classList.add('checked');
	} else if (wrAvg >= 2.5) {
		wrDiv.querySelector('#wr2').classList.add('checked');
		wrDiv.querySelector('#wr3').classList.add('checked');
	} else if (wrAvg >= 1.5) {
		wrDiv.querySelector('#wr2').classList.add('checked');
	}
});

/* Listening for clicks on Read later and removing script from that list */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#mp_read_later_view').addEventListener('click', function(e) {
        const tgt = e.target.closest('.js_remove_rl');
        if (tgt) {
			const rlDiv = tgt.closest('.mp_script_container');
            const rlid = rlDiv.querySelector('.js_script_id').value; 
            fetch(`/read_later/${rlid}`, {
                method: 'POST',
                body: JSON.stringify({
                  action: 'remove'
                })
              }).then (function() {
                    rlDiv.style.display = 'none';
              });
        }
    });
});

/* Listening for click on Reading and removing script from that list when user is done reading */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#mp_reading_view').addEventListener('click', function(e) {
        const tgt = e.target.closest('.finish_reading');
        if (tgt) {
			const rDiv = tgt.closest('.mp_script_container');
            const rid = rDiv.querySelector('.js_script_id2').value; 
            fetch(`/finish_reading/${rid}`, {
                method: 'POST',
                body: JSON.stringify({
                  action: 'finish'
                })
              }).then (function() {
                    rDiv.style.display = 'none';
              });
        }
    });
});