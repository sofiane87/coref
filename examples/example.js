var template = '<div class="input-group"></div>',
    kw_field = '<label for="KeyWord">Keyword</label><input type="text" class="form-control" id="KeyWord"/>'
    cb_field = '<label for="CaseSensitive">Case sensitive</label><input class="form-control" type="checkbox" id="CaseSensitive"/>'
    minusButton = '<span class="btn input-group-addon delete-field">(-)</span>';

$('.add-field').click(function() {
    var temp = $(template).insertBefore('.btn-primary');
    temp.append(kw_field);
    temp.append(cb_field);
    temp.append(minusButton); });

$('.fields').on('click', '.delete-field', function(){
    $(this).parent().remove(); });
