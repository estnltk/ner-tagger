function Timer() {
    var self = this;
    self.milliseconds = 0;
    self.timer;
    self.ontick_callback;
    self.pause = function () {
        clearInterval(self.timer);
    };
    self.resume = function () {
        self.start();
    };
    self.reset = function () {
        self.milliseconds = 0;
        if (self.timer != undefined)
            clearInterval(self.timer);
        self.start();
    };
    self.start = function () {
        self.timer = setInterval(function () {
            self.milliseconds += 100;
            if (self.ontick_callback != undefined)
                self.ontick_callback(self.milliseconds);
        }, 100);
    };
    self.ontick = function (callback) {
        self.ontick_callback = callback;
    };
}

function View() {
    var self = this;
    self.set_controller = function (controller) {
        self.controller = controller;
        $('.btn-lbl').click(controller.annotate_sentence);
        $('#btn-skip').click(controller.skip_sentence);
        $('#btn-timer').click(function () {
            if ($('#btn-timer').attr("data-action") == "resume") {
                $('#btn-timer .glyphicon').removeClass('glyphicon-play');
                $('#btn-timer .glyphicon').addClass('glyphicon-pause');
                $('#btn-timer').attr("data-action", "pause");
                controller.resume_timer();
            }
            else { // pause
                $('#btn-timer .glyphicon').removeClass('glyphicon-pause');
                $('#btn-timer .glyphicon').addClass('glyphicon-play');
                $('#btn-timer').attr("data-action", "resume");
                controller.pause_timer();
            }
        });
        $("body").keypress(function (e) {
            var btn;
            if (e.which == 97) // a
                btn = $('#btn-lbl-loc');
            else if (e.which == 100) // d
                btn = $('#btn-lbl-org');
            else if (e.which == 115) // s
                btn = $('#btn-lbl-per');
            else if (e.which == 106) // j
                btn = $('#btn-lbl-o');
            else if (e.which == 107) // k
                btn = $('#btn-lbl-fac');
            else if (e.which == 108) // l
                btn = $('#btn-lbl-prd');
            else if (e.which == 32) // space
                btn = $('#btn-skip');

            if (btn != undefined) {
                btn.addClass("active");
                btn.trigger("click");
                setTimeout(function () {
                    btn.removeClass("active");
                }, 150);
            }
        });
    };
    self.update = function (state) {
        var snt = state.get_current_sentence();
        var marked_sentence = annotate_entity_in_sentence(snt['text'], snt['entity_start'], snt['entity_end']);
        $('#sentence').html(marked_sentence);
        $('#entity').html(snt['entity_text']);
        $('#buttons .btn').blur().removeClass('btn-warning');
        for (i = 0; i < 2; i++) {
            $("#buttons").find("[data-category='" + snt["entity_categories"][i] + "']").addClass('btn-warning');
        }

    };
    self.update_time = function (msecs) {
        /* Update displayed time ever second */
        $('#timer').html(Math.floor(msecs / 1000));
    }
}

function annotate_entity_in_sentence(snt, e_start, e_end) {
    return snt.substring(0, e_start) + '<span class="snt-entity">' + snt.substring(e_start, e_end) + '</span>' + snt.substring(e_end, snt.length);
}

function State(sentences, cur_snt) {
    var self = this;
    self.sentences = sentences;
    self.cur_snt = cur_snt;
    self.reset = function () {
        self.cur_snt = 0;
        self.sentences = [];
    };
    self.get_current_sentence = function () {
        return self.sentences[self.cur_snt];
    };
    self.increment = function () {
        self.cur_snt += 1;
    };
    self.is_last_sentence = function () {
        return self.cur_snt == self.sentences.length - 1;
    };
    self.annotate_sentence = function (category, time) {
        var snt = self.sentences[self.cur_snt];
        snt["category"] = category;
        snt["time"] = time;
    };
}

function Controller() {
    var self = this;
    self.timer = new Timer();
    self.timer.ontick(function (s) {
        if (self.view != undefined)
            self.view.update_time(s);
    });
    self.set_view = function (view) {
        self.view = view;
    };
    self.pause_timer = function () {
        self.timer.pause();
    };
    self.resume_timer = function () {
        self.timer.resume();
    };
    self.load_data = function () {
        $.ajax({
                url: '/load-sentences-view/',
                method: 'post',
                data: {'corpus_id': get_corpus_id_from_url()},
                cache: false
            })
            .done(self.data_loaded)
            .fail(function (err) {
                alert(err['statusText']);
            });
    };
    self.data_loaded = function (data) {
        if (data.length == 0) {
            alert('Terve korpus on märgendatud!');
            window.location = '/';
        }
        else {
            self.state = new State(data, 0);
            self.view.update(self.state);
            self.timer.reset();
        }
    };
    self.pick_next_sentence = function () {
        if (self.state.is_last_sentence()) {
            var snts = _.map(self.state.sentences, function (s) {
                return {
                    "id": s['id'],
                    "entity_annotation_id": s["entity_annotation_id"],
                    "marked_category": s["category"],
                    "time": s["time"],
                    "entity_categories": s["entity_categories"],
                    "corpus_id": get_corpus_id_from_url()
                };
            });
            self.state.reset();
            $.ajax({
                url: '/submit-sentences-view/',
                method: 'post',
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify(snts)
            }).fail(function (err) {
                alert('Failed to submit word data. Error: ' + err["status"] + ' ' + err["statusText"]);
            }).done(self.data_loaded);
        }
        else {
            self.state.increment();
            self.view.update(self.state);
            self.timer.reset();
        }
    };
    self.annotate_sentence = function () {
        self.timer.pause();
        self.view.update_time(0);
        var category = $(this).attr("data-category");
        self.state.annotate_sentence(category, self.timer.milliseconds);
        self.pick_next_sentence();
    };
    self.skip_sentence = function () {
        self.timer.pause();
        self.view.update_time(0);
        self.state.get_current_sentence()["time"] = self.timer.milliseconds;
        self.pick_next_sentence();
    };
}

function get_corpus_id_from_url() {
    var corpus_id_regexp = /(\d+)\/?$/;
    var match = corpus_id_regexp.exec(window.location.href);
    var corpus_id = match[1];
    return corpus_id;
}

$(document).ready(function () {
    var view = new View();
    var controller = new Controller();
    view.set_controller(controller);
    controller.set_view(view);
    controller.load_data();
});
