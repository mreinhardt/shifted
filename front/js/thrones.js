var onCharactersLoad, thrones;

onCharactersLoad = function(characters) {
    thrones = new Ractive({
        el: '#thrones',
        template: '#characters',
        data: {
            characters: characters,
            sort: function(chars, sortCol) {
                chars = chars.slice(0);
                return chars.sort(function(a, b) {
                    return a[sortCol] < b[sortCol] ? -1 : 1;
                });
            },
            sortCol: 'name'
        }
    });

    thrones.on('sort', function(ev, col) {
        var $th = $('#thrones .characters th');
        this.set('sortCol', col);
        $th.removeClass('sorted');
        $th.filter('.' + col).addClass('sorted');

    });

    thrones.observe('houseFilter', function (newVal, oldVal) {
        this.set('characters', characters.filter(function(d) {
            return d.house.toLowerCase().indexOf(newVal.toLowerCase()) > -1;
        }));
    });

    thrones.on('addCharacter', function(ev) {
        ev.original.preventDefault();

        var $form = $(ev.node),
            attrs = $form.serializeArray(),
            character = {};

        $.each(attrs, function(i, attr) {
            character[attr['name']] = $.trim(attr['value']);
        });

        characters.push(character);

        $form.get(0).reset();
    });
};

$.getJSON('characters.json', onCharactersLoad);
