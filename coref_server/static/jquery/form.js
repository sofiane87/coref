$(document).ready(function () {
    var counter = 0;

    $("#addrow").on("click", function () {
        counter++;
        var newField = $('<div class="form-row align-items-center" id="Expression' + counter + '">');
        var cols = '<div class="col-auto"> <input name="expression_' + counter + '" id="inlineFormInput' + counter + '" class="form-control mb-2" type="text" placeholder="Expression"/></div>';
        cols += '<div class="col-auto"><div class="form-check mb-2"><input name="case_sensitive_' + counter + '" id="autoSizingCheck' + counter + '" class="form-check-input" type="checkbox"/> <label class="form-check-label" for="autoSizingCheck' + counter + '"> Case sensitive </label>  </div></div>';
        cols += '<div class="col-auto"><button class="btn btn-info mb-2" id="BtnDelete' + counter +'">Delete</button></div>';
        newField.append(cols);
        $("#ExpressionForm").append(newField);

        var local_counter = counter

        $("#BtnDelete" + local_counter).on("click", function () {
            $("#Expression" + local_counter).remove();
        });
    });


    $("#analyse_btn").on("click", function() {
      var target_text = $("textarea#TextToAnalyse").val();
      var form_fields = $("form#ExpressionForm").serializeToJSON();
      console.log({"text": target_text, "form": form_fields});
        $.ajax({
            "url": "/analyse",
            "type": "GET",
            "dataType": "json",
            "data": {"result": JSON.stringify({"text": target_text, "expressions": form_fields})},
            "success": function(result) {
                $("div#text_output").html(result["html"])
            },
            error: function(xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
        })
    })


});
