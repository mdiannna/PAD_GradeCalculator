// clear_students_list_js();
$( document ).ready(function() {
	show_students_list();
	append_students_select();
});

function get_nr_students() {
	var nr_students = parseInt(localStorage.getItem('nr_students'));
	return nr_students;
}

function get_students_list() {
	var result = [];
	var nr_students = parseInt(localStorage.getItem('nr_students'));


	for (var i=1; i<=nr_students; i++) {
		var student_name = localStorage.getItem('student' + i);
		var group = localStorage.getItem('grupa-student' + i);
		result[i-1] = {"NumePrenume":student_name, "Grupa":group};
	}
	return result;
}

function show_students_list() {
	var students_list = get_students_list();
	$("#students_list_div").empty();

	$("#students_list_div").append("<b>Student, Grupa</b><br>");
	$.each(students_list, function(index, value){
        // $("#students_list_div").append("Student:" + value["NumePrenume"] + "   Grupa:" + value["Grupa"] + '<br>');
        $("#students_list_div").append(index+1 + "." + value["NumePrenume"] + ", " + value["Grupa"] + '<br>');
    });
}


function append_students_select() {
	var students_list = get_students_list();

	$.each(students_list, function(index, value){
        $("#students_list_select").append(new Option(value["NumePrenume"] + "," + value["Grupa"], value["NumePrenume"]) );
    });
}

function add_student() {
	nr_students = get_nr_students()+1;
	localStorage.setItem('nr_students', nr_students);

	var nume_prenume = $("#nume_prenume_add_student").val();
	var group = $("#grupa_add_student").val();

	// alert("nr students:" + nr_students);

	localStorage.setItem('student' + nr_students, nume_prenume);
	localStorage.setItem('grupa-student' + nr_students, group);

	alert("Student added!");
	
	$("#nume_prenume_add_student").val('');
	$("#grupa_add_student").val('');


    show_students_list();
    append_students_select();
}


function clear_students_list_js() {
	localStorage.setItem('nr_students', 0);
}