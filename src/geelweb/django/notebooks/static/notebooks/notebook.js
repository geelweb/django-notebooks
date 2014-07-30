var storage = localStorage;

$('.add-to-notebook').click(function() {
    var app = $(this).data('app'),
        model = $(this).data('model'),
        object_id = $(this).data('id'),
        store_url = $(this).data('store-url');

    var key = [app, model].join('-'),
        item = {'app': app, 'model': model, 'object_id': object_id},
        collection = JSON.parse(storage.getItem(key));

    jQuery.get(store_url);

    if (!collection) collection = [];

    var exists = false;
    collection.filter(function(aElement, aIndex, aArray) {
        if (aElement.object_id == item.object_id) {
            exists = true;
            return false;
        }
        return true;
    });

    if (!exists) {
        collection.push(item);
        storage.setItem(key, JSON.stringify(collection));
    }
});

(function($) {
    $.fn.notebook = function() {
        return this.each(function() {
            var app = $(this).data('app'),
                model = $(this).data('model'),
                url = $(this).data('url'),
                load_url = $(this).data('load-url');

            var self = this;

            jQuery.get(load_url, function(collection) {
                if (collection.length > 0) {
                    for (var i=0; i<collection.length; i++) {
                        jQuery.get(url, {'pk': collection[i].fields.object_id}, function(data) {
                            $(self).append(data);
                        });
                    }
                } else {

                    var key = [app, model].join('-'),
                        collection = JSON.parse(storage.getItem(key));

                    if (!collection) return;


                    for (var i=0; i<collection.length; i++) {
                        jQuery.get(url, {'pk': collection[i].object_id}, function(data) {
                            $(self).append(data);
                        });
                    }
                }
            });
        });
    };

    $(document).ready(function() {
        $('ul.notebook-collection').notebook();
    });
}(jQuery));

