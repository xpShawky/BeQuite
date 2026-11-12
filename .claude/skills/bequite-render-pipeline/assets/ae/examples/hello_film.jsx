// hello_film.jsx - minimal starter build: proves the bridge, the libraries and the render queue on a new machine.
// Copy assets/ae/* into the project's ae/ folder, then:   node ae/runae.js ae/examples/hello_film.jsx --timeout 300
// It builds an 8 s, 1920x1080, 60 fps comp with three kinetic-type treatments, queues a render, saves the .aep and
// writes review stills. Nothing is rendered by this script; rendering is a separate, approved step (aerender.js).
$.evalFile(new File(AE_ROOT + "/lib/core.jsx"));
$.evalFile(new File(AE_ROOT + "/lib/type.jsx"));

// Tokens normally come from the film's Motion DNA. Fonts must be installed; use PostScript names.
K.config({ name: "hello-film", W: 1920, H: 1080, FPS: 60,
           C: { paper: "#F2F2F2", ink: "#1A1A1A", acc: "#2F6BFF" } });
app.beginUndoGroup("hello film");
K.newProject({ name: "hello-film" });

var DUR = 8;
var film = K.comp("FILM", DUR, 0, 0, K.C.paper);
K.bg(film, "light", 0);

// 1) headline: character write-on with blur, rise and a soft bounce; slow push while it holds
var a = K.say(film, [["Every line gets ", 0], ["a treatment.", 1]], 960, 560, 0.4, 1.0, { size: 96 });
K.push(film, a.layers, 960, 530, 0.4, 2.9, 2);
a.out(2.9);

// 2) list / alternatives: one slot swaps its word while the line re-centres
var s = K.swapLine(film, [["Made for ", 0]], [["calm.", 1], ["focus.", 1], ["you.", 0]], 960, 560, 3.3, [3.6, 4.7, 5.8], { size: 96 });
s.out(6.9);

// 3) one key word: recolour sweep (plain -> accent) on the last word, after it has landed
K.recolor(s.words[2].layers[0], 6.2, 0.4, K.C.acc);

var out = new Folder(AE_ROOT + "/build/render"); if (!out.exists) out.create();
var rq = app.project.renderQueue.items.add(film);
rq.applyTemplate("Best Settings");
rq.outputModule(1).file = new File(out.fsName + "/hello_film.mov");   // output template left at the AE default
app.endUndoGroup();

var aep = new File(AE_ROOT + "/build/hello_film.aep");
app.project.save(aep);
var shots = K.stills(film, [0.8, 1.6, 4.0, 6.5], AE_ROOT + "/build/stills_hello");
RESULT = { saved: aep.fsName, stills: shots, renderQueueItems: app.project.renderQueue.numItems };
