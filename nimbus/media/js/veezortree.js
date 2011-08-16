$(document).ready(function(){
    // Tudo começa aqui
	TREES = find_containers();
	for (var t = 0; t < TREES.length; t++) {
		create_tree(TREES[t]);
	};
});
function find_containers() {
    // encontra os objetos da classe veezortree
	var TREES = new Array();
	for (var o = 0; o < $(".veezortree").length; o++) {
		Tree = new Object();
		Tree.CONTAINER = $(".veezortree")[o].id;
		Tree.CHECK_TYPE = $(".veezortree")[o].attributes["check_type"].value;
		Tree.computer = $(".veezortree")[o].attributes["computer"].value;
		if ($(".veezortree")[o].attributes["is_windows"].value == "true") {
			Tree.IS_WINDOWS = true;
		} else {
			Tree.IS_WINDOWS = false;
		};
		if ($(".veezortree")[o].attributes["hide_files"].value == "true") {
			Tree.HIDE_FILES = true;
		} else {
			Tree.HIDE_FILES = false;
		};
		Tree.ITEM_INDEX = 0;
		TREES.push(Tree);				
	}
	return TREES;
}
function create_tree(Tree) {
	if (Tree.IS_WINDOWS == true) {
		var path = "";
		var click_event = "fetch_dir_content('" + Tree.CONTAINER + "', '" + path + "', '" + Tree.computer + "', '" + Tree.CONTAINER+Tree.ITEM_INDEX + "')"
		var new_line = "<li class='directory'id='li_" + Tree.CONTAINER+Tree.ITEM_INDEX + "'>" +
						"<input type='" + Tree.CHECK_TYPE + "' disabled='disabled'><span class='end_path' onClick=\"" + click_event + "\">Meu computador" +
						"</span></li><ul id='" + Tree.CONTAINER+Tree.ITEM_INDEX + "'>" + 
						"</ul>"
	} else {
		var path = "/";
		var click_event = "fetch_dir_content('" + Tree.CONTAINER + "', '" + path + "', '" + Tree.computer + "', '" +Tree.CONTAINER+Tree.ITEM_INDEX + "')"
		var new_line = "<li class='directory'id='li_" + Tree.CONTAINER+Tree.ITEM_INDEX + "'>" +
						"<input type='" + Tree.CHECK_TYPE + "' name='"+ Tree.CONTAINER +"_restore_path' value=\"" + path + "\"></input><span class='end_path' onClick=\"" + click_event + "\">/" +
						"</span></li><ul id='" + Tree.CONTAINER+Tree.ITEM_INDEX + "'>" + 
						"</ul>"
	};
	$("#" + Tree.CONTAINER).append(new_line);
	Tree.ITEM_INDEX++;
};
function find_tree_object(container) {
	for (var t = 0; t < TREES.length; t++) {
		if (TREES[t].CONTAINER == container) {
				return TREES[t];
		}
	};
	return false;
};
function fetch_dir_content(container, path, computer, id) {
	console.log(container, path, computer, id);
	var Tree = find_tree_object(container);
	ul_of_this_item = $("#" + id);
	this_item_li = $("#li_" + id);
	if (ul_of_this_item.hasClass("open") == true) {
		ul_of_this_item.hide("slow");
		ul_of_this_item.removeClass("open")
		this_item_li.removeClass("open");
		return false;
	} else {
		ul_of_this_item.addClass("open");
		this_item_li.addClass("open");
		ul_of_this_item.show("slow");
		if (ul_of_this_item.hasClass("filled") == true) {
			return false;
		};
		ul_of_this_item.addClass("filled");
	}
	if ($("#wait")[0] != undefined) {
		return false
	} else {
		$("#" + Tree.CONTAINER).append("<div id='wait'>Aguarde <img src='/media/icons/loading_bar.gif'/></div>");
	}
	$.ajax({
		type: "POST",
		// async: false,
		url: "http://192.168.50.129/filesets/get_tree/",
		data: "computer_id=" + computer + "&path=" + path,
		dataType: "json",
		success: function(file_list) {
			console.log(file_list);
			for (var i in file_list) {
				var full_path = file_list[i];
				if (full_path[full_path.length -1] == "/") {
					var click_event = "fetch_dir_content('" + Tree.CONTAINER + "', '" + full_path + "', '" + computer + "', '" + Tree.CONTAINER+Tree.ITEM_INDEX + "')"
					var location_type = "directory";
				} else {
					var click_event = ""
					var location_type = "file";
				}
				var new_path = full_path.slice(path.length);
				var new_line = "<li class='" + location_type + "'id='li_" + Tree.CONTAINER+Tree.ITEM_INDEX + "'>" +
								"<input type='" + Tree.CHECK_TYPE + "' name='"+ Tree.CONTAINER +"_restore_path' value=\"" + full_path + "\"></input><span class='end_path' onClick=\"" + click_event + "\">" + new_path +
								"</span></li><ul id='" + Tree.CONTAINER+Tree.ITEM_INDEX + "'>" + 
								"</ul>"
				if ((Tree.HIDE_FILES == false) || (location_type != "file")) {
					ul_of_this_item.append(new_line);
				} 
				Tree.ITEM_INDEX++;
			}
			$("#wait").remove();
		}
	});
};