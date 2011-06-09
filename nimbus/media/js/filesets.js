$(document).ready(function(){
    $('#filepath_template').clone().appendTo('.filepaths').show();
    
    $('.toggle').click(function(){
        var target = $(this).attr('ref');
        $(this).parent().parent().find('.' + target).slideToggle();
    });
    
    get_tree_path = "/filesets/get_tree/";
    
    $('#update_tree').click(function()
    {
        update_tree('/', get_tree_path);
        return false;
    });
    
    $(".tree a").click(function() {
        if (!document.getElementsByClassName('wait')[0]) {
            update_tree($(this).attr("path"), get_tree_path);
        } else {
            $('.wait').remove();
        }
        return false;
    });
    
    function adicionar_path(obj) {
        if (obj) {
            $('#filepath_template').clone().insertAfter($(obj).parent()).show();
        } else {
            $('#filepath_template').clone().appendTo('.filepaths').show();
        }
        
        $('.filepaths .add').click(function(){
            adicionar_path(this);
        });
        
        $('.filepaths .del').unbind('click').click(function(){
            remover_path(this);
        });
    }
    
    function remover_path(obj) {
        $(obj).parent().remove();
        if ($('#filepath_template').parent().children().length == 1) {
            adicionar_path();
        }
    }

    $('.filepaths .add').click(function(){
        adicionar_path(this);
    });

    $('.filepaths .del').click(function(){
        remover_path(this);
    });

    $('#computer_id').change(function(){
        $('.tree > li ul').first().remove();
    });
    
    
});
$(document).ready(function(){
    $('#submit_button').click(function(){
		var all_paths = $('.full_path');
		var checked_paths = new Array()
		for (var i = 0; i < all_paths.length; i++) {
			if (all_paths[i].checked == true) {
				checked_paths.push(all_paths[i].value);
			};
		};
		console.log(checked_paths);
		$('#id_files-TOTAL_FORMS').val(checked_paths.length);
		for (var n = 0; n < checked_paths.length; n++) {
			var new_path_field = '\n' + 
			'<input id="id_files-'+ n + '-path" type="hidden" name="files-'+ n +'-path" maxlength="2048" class="text" value="' + checked_paths[n] + '">\n' +
			'<input type="hidden" name="files-' + n + '-fileset" id="id_files-' + n + '-fileset">\n' +
			'<input type="hidden" name="files-' + n + '-id" id="id_files-' + n + '-id">\n';
			$('#main_form').append(new_path_field);
		};
		if (checked_paths.length > 0) {
		    $('#main_form').submit();
        } else {
            alert('Você deve escolher algum arquivo');
        }
	});
});
