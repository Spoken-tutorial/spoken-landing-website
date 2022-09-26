$(document).ready(function(){
    $('.create_zip').prop('disabled', true); 

    // clear level & language field on selecting new foss
    $('.foss_category').on("change", function(){
                $('.level').val('');
                $('.language').html('');
                if($('.foss_category').val() == '') {
                    $('.level').attr("disabled", "disabled");
                    $('.language').attr("disabled", "disabled");
                }else {
                    $('.level').removeAttr('disabled');
                }
    });
    // clear level & language field on selecting new foss end

    $('.level').on("change", function(){
        var foss = $('.foss_category').val();
        var level = $(this).val();
        $('.language').html('');
        $('.language').attr("disabled", "disabled");
        if(foss && level) {
            $.ajax({
                url: "/cdcontent/ajax-fill-languages/",
                type: "POST",
                data: {
                    foss: foss,
                    level: level
                },
                beforeSend: function() {
                    $('.ajax-refresh-language').show();
                },
                success: function(data) {
                    // loading languages
                    if(data) {
                        $('.language').html(data);
                        $('.language').removeAttr('disabled');
                    }
                    $('.ajax-refresh-language').hide();
                }
            });
        }
    });

    $('.add_foss_lang').on("click", function(){
        $('.added-foss').show();
        foss = $('.foss_category').val();
        level = $('.level').val();
        langs = JSON.stringify($('.language').val());
        selectedfoss = $('.selected_foss').val();
        if(foss && langs && level) {
            $.ajax({
                url: "/cdcontent/ajax-add-foss/",
                type: "POST",
                data: {
                    foss: foss,
                    langs: langs,
                    level: level,
                    selectedfoss: selectedfoss,
                },
                beforeSend: function() {
                    $('.add_foss_lang').css('display', 'none');
                    $('.ajax-refresh-add-foss').show();
                },
                success: function(data) {
                    data = JSON.parse(data);
                    console.log('data');
                    console.log(data);
                    if(data) {
                        data = JSON.stringify(data);
                        if(data != '{}') {
                            $('.selected_foss').val(data);
                             selectedfoss = $('.selected_foss').val();
                        } else {
                            $('.selected_foss').val('');
                        }
                    }
                    selectedfoss: $('.selected_foss').val();
                    show_added_foss(selectedfoss);
                    $('.ajax-refresh-add-foss').hide();
                    $('.add_foss_lang').show();
                }
            });
            $('.add_foss_lang').show();
            $('.ajax-refresh-add-foss').hide();
        }
    });

    $(".cdcontentform").on( "submit", function(event) {
                event.preventDefault();
                var url = $(location).attr('href');
                $('.download-link').html('<i class="fa fa-circle-o-notch fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span> please do not refresh the page, we are preparing your download link');
                var posting = $.post(url, $(this).serialize());
                posting.done(function(data) {
                    if(data.status) {
                        var downloadLink = '<a href="' + data.path + '" title="Download CD Content Zip" id="download-zip-btn"  class="btn btn-success">Download CD Content</a>';
                        var message = 'You are part of our paid service.<br> Happy Downloading.'
                        $('.download-link').html(downloadLink);
                        $('.user-message').html(message);
                    } else {
                        var message = 'Somethings went wrong! please refresh the page and try again.'
                        $('.download-link').html(message);
                    }
                });
                posting.fail(function() {
                    var message = 'Something went wrong! please refresh the page and try again.'
                    $('.download-link').html(message);
                });
    });

    $('#download_btn').click(function() {
        $('#paymodal').modal('hide');
        $('#rate-div').hide();
    });
    
});

function delete_foss(elem){
    var foss_id = elem.parentNode.id;
    var foss_lang_obj = JSON.parse(selectedfoss);
    var foss_to_delete = foss_lang_obj[foss_id];
    var langs = foss_to_delete[0];
    var size = foss_to_delete[1];
    delete foss_lang_obj[foss_id];
    selectedfoss = JSON.stringify(foss_lang_obj);
    $('.selected_foss').val(selectedfoss);
    var add_foss_btn = document.getElementsByClassName("add_foss_lang");
    show_added_foss(selectedfoss);
    if (Object.keys(foss_lang_obj).length === 0) {
        $('.added-foss').hide();
        document.getElementById("amount_to_pay").value = '0';
    }
    $('.ajax-refresh-add-foss').hide();
    $('.add_foss_lang').show();
}

function show_added_foss(selected_foss){
    $.ajax({
        url: "/cdcontent/ajax-show-added-foss/",
        type: "POST",
        data: {
            selectedfoss : selected_foss,
        },
        beforeSend: function() {
            $('.add_foss_lang').css('display', 'none');
            $('.ajax-refresh-add-foss').show();
        },
        success: function(data) {
        header = '<caption class="col-left"><b>Selected FOSS List:<span class="pull-right"> ~ Total Size : '+data[1]+'</span></b></caption><tr ><th>FOSS</th><th>Level</th><th>Languages</th><th>Size</th>';
        if(data) {
            $('.added-foss').html(header + data[0]);
                                    
        var foss_table = document.getElementById("added-foss");
        var row_count = document.getElementById("added-foss").rows.length;
        for (var i = 0 ;i < row_count; i++) {
            var x = document.getElementById("added-foss").rows[i].cells.length;
            if (x==5) {
                var content = '<button type="button" class="btn delete-btn" class="delete-foss" onclick="delete_foss(this)"><i class="fa fa-trash-o"></i></button>'
                var td = document.getElementById("added-foss").rows[i].cells[4];
                td.innerHTML = content;   
            }    
        }
        if(data[2][0]=='UR') {
        var message = ''
         $('.create_zip').prop('disabled', true);
         $('.user-message').html(message);
         $('.download-a').html("Download");
         $("#rate-div").show();
         // $("#user_file_size").html("Foss Purchase (INR)");
        document.getElementById("amount_to_pay").value = data[2][1];
        }
        if(data[2][0]=='RP') {
        var message = 'You are part of our paid service.<br> Happy Downloading.<br> Please click on <b>Create Zip file</b> to proceed.'
         $('.create_zip').prop('disabled', false);
         $('.user-message').html(message);
         $('.download-a').html("Download");
         $("#rate-div").hide();
         $('.user-message').addClass("user-message-highlight");
        }
        else {
         $('.create_zip').prop('disabled', true);
         $('.user-message').html(message);
         $('.download-a').html("Download");

         $("#rate-div").show();
         // $("#user_file_size").html("Foss Purchase (INR)");
         document.getElementById("amount_to_pay").value = data[2][1];
        }
        if (Object.keys(JSON.parse(selectedfoss)).length === 0) {
            document.getElementById("amount_to_pay").value = '0';
        }
        }
        $('.ajax-refresh-add-foss').hide();
        }
    });
}






