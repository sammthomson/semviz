
// Nathan Schneider
// 2010-06-01
// 2010-09-09: v.0.1
// 2011-12-01: v.0.2: removed the use of E4X, fixed the file API to be compatible with Firefox 8
// 2013-04-13: v.0.3: use JSON input instead of XML
// 2015-12-03: v.0.4: use (or convert to) SEMAFOR 3-style "spans" array in JSON
// 	(backward-compatible; untested for multiple spans, i.e. discontinuous target
//  or frame element)
// 2015-12-21: v.0.5: actually ensure backward-compatibility of JSON format;
//  correctly display an argument span covering a subrange of the target span;
//  remove old code from XML days



try {
	console.log("console activated");
}
catch (ex) {
	console = {log: function (msg) { }, error: function (msg) { }, warn: function (msg) { }};
}



// Given a sorted list l, return the index of the smallest value that is not greater than v
function argNearestLowerBound(l, v) {
	for (var i=0; i<l.length; i++) {
		if (l[i]>v)
			return i-1;
	}
	return l.length-1;
}

function getRangeFromClassAttr(attValue, rangePrefix) {
	var a = " "+attValue+" ";
	var i = a.indexOf(" "+rangePrefix);
	var j = a.indexOf(":", i);
	var k = a.indexOf(" ", j);
	var r = [Number(a.substring(i+2,j)), Number(a.substring(j+1,k))];
	return r;
}

/*	// The following JSON is in the style produced by SEMAFOR 2.
	  // SEMAFOR 3 indicates spans of each target or frame element
		// with a "spans" list, each element of which is an object
		// containing "start", "end", and "text" attributes.
		// buildSentence() converts input to the new style if necessary.
{
  "tokens": [
    "Little",
    "Miss",
    "Muffet",
    "sat",
    "on",
    "a",
    "tuffet",
    ",",
    "eating",
    "her",
    "curds",
    "and",
    "whey",
    "."
  ],
  "frames": [
    {
      "target": {
        "start": 1,
        "end": 2,
        "name": "Success_or_failure",
        "text": "Miss"
      },
      "annotationSets": [
        {
          "frameElements": [],
          "score": 50.67000167192763,
          "rank": 0
        }
      ]
    },
    {
      "target": {
        "start": 3,
        "end": 4,
        "name": "Being_located",
        "text": "sat"
      },
      "annotationSets": [
        {
          "frameElements": [
            {
              "start": 2,
              "end": 3,
              "name": "Theme",
              "text": "Muffet"
            },
            {
              "start": 4,
              "end": 13,
              "name": "Location",
              "text": "on a tuffet , eating her curds and whey"
            }
          ],
          "score": 26.113001442959114,
          "rank": 0
        }
      ]
    },
    {
      "target": {
        "start": 8,
        "end": 9,
        "name": "Ingestion",
        "text": "eating"
      },
      "annotationSets": [
        {
          "frameElements": [
            {
              "start": 9,
              "end": 13,
              "name": "Ingestibles",
              "text": "her curds and whey"
            }
          ],
          "score": 32.136330321065294,
          "rank": 0
        }
      ]
    }
  ]
}
*/

function buildSentence(sJ,sTag) {
	var ww = sJ["tokens"];
	$sN = $('<table class="sentence"><tr><th class="w0"/></tr></table>');

	// Row for frame names under targets
	var $trtN = $('<tr class="frameann below targets"></tr>');	// TODO: distinguish above/below

	for (var iw=0; iw<ww.length; iw++) {
		$sN.find('tr').eq(0).append('<th class="word w'+iw+'">'+ww[iw]+'</th>');
	}


	var rows = [];
	var targets = [];	// word offset => annotation ID
	var frames = [];	// annotation ID => frame name
	var aId = 0;	// annotation ID
	var framesJ = sJ["frames"];
	framesJ.sort(function (a,b) {	// sort by target word index
		return (a["target"]["start"]>b["target"]["start"]) ? 1 : ((a["target"]["start"]===b["target"]["start"]) ? 0 : -1);
	});
	for (var i=0; i<framesJ.length; i++) {	// for each frame instance
		var ann = framesJ[i];



		var aTag = sTag + 'a'+aId;
		ann["target"]["type"] = "target";
		var fname = ann["target"]["name"];
		frames[aId] = fname;
		var fTag = 'f'+fname;

		// mark each word in the target span and store it in 'targets'
		if (!ann["target"]["spans"]) {
			ann["target"]["spans"] = [{"start": ann["target"]["start"],
																 "end": ann["target"]["end"],
																 "text": ann["target"]["text"]}];
		}
		for (var isp=0; isp<ann["target"]["spans"].length; isp++) {
			var span = ann["target"]["spans"][isp];
			var st = span["start"];
			var en = span["end"];
			var r = st + ':' + en;
			for (var iw=st; iw<en; iw++) {
				var $wN = $sN.find('tr').eq(0).find('th.w'+iw);	// word in the target span
				//console.log($wN);
				$wN.addClass('target '+fTag);
				var curTitle = $wN.attr("title");
				curTitle = (curTitle) ? curTitle+' ' : '';
				$wN.attr("title", curTitle + fname);
				targets[iw] = aId;
			}
		}




		// Row for the annotation
		var $trN = $('<tr id="' + aTag+'" class="frameann below"></tr>');

		// target label + FEs
		var labels = ann["annotationSets"][0]["frameElements"];	// TODO: can a frame have multiple annotationSets?
		labels.push(ann["target"]);

		// Convert to SEMAFOR 3-style target and FE spans
		labels.forEach(function (label) {
			if (!label["spans"]) {
				label["spans"] = [{"start": label["start"],
													"end": label["end"],
													"text": label["text"]}];
			}
			else {
				// attributes of label as a whole, assuming spans are sorted
				label["start"] = label["spans"][0]["start"];
				label["end"] = label["spans"][label["spans"].length-1]["end"];
				var tokens = [];
				label["spans"].forEach(function (span) {
					tokens.push(span["text"]);
				});
				label["text"] = tokens.join(" ");
			}
		});

		labels.sort(function (a,b) {	// sort this frame's FE and target labels by start index,
		// secondarily by end index, and tertiarily putting targets before arguments
			if (a["spans"][0]["start"]==b["spans"][0]["start"]) {
				if (a["spans"][0]["end"]==b["spans"][0]["end"]) {
					return (a["type"]=="target") ? ((b["type"]=="target") ? 0 : -1) : 1;
				}
				return a["spans"][0]["end"]-b["spans"][0]["end"];
			}
			return a["spans"][0]["start"]-b["spans"][0]["start"];
		});

		// Attempt to deal with span containment: if span 1 starts before span 2,
		// and continues after the start of span 2, split off the part of span 1
		// that overlaps with span 2 as well as the part that continues past span 2 (if applicable)
		for (var j=labels.length-1; j>0; j--) {
			if (labels[j-1]["start"]<labels[j]["start"] && labels[j]["start"]<labels[j-1]["end"]) {
				if (!labels[j-1]["type"]) {
					console.error('Unexpected: overlap but previous label has no type');
					console.log(labels[j-1]);
					console.log(labels[j]);
				}
				if (labels[j]["end"]<labels[j-1]["end"]) {
					// insert at position j+1: continuation after span 2
					labels.splice(j+1, 0, {"type": labels[j-1]["type"], "start": labels[j]["end"],
																 "end": labels[j-1]["end"],
																 "text": labels[j-1]["text"], "name": labels[j-1]["name"],
																 "continuation": true});
				}
				// insert at position j: part of span 1 overlapping with span 2
				labels.splice(j, 0, {"type": labels[j-1]["type"], "start": labels[j]["start"],
														 "end": Math.min(labels[j-1]["end"],labels[j]["end"]),
														 "text": labels[j-1]["text"], "name": labels[j-1]["name"],
														 "continuation": true,
													 	 "continues": (labels[j]["end"]<labels[j-1]["end"])});
				// narrow the original span 1
				labels[j-1]["end"] = labels[j]["start"];
				labels[j-1]["continues"] = true;
			}
		}


		// construct a row for this frame's spans
		// TODO: not tested for discontinuous targets or FEs (where the "spans" array has multiple elements)
		var wi = 0;
		var maxwen = -1;

		for (var k=0; k<labels.length; k++) {
			// start and end of the label as a whole
			var wst = labels[k]["start"]+1;
			var wen = labels[k]["end"]+1;
			//for (var ispan=0; ispan<labels["spans"].length; ispan++) {

				if (wen>maxwen)
					maxwen = wen;
				if (wi<wst) {	// insert filler cell
					var c = (k>0) ? "internalFiller" : "framename";
					$trN.append('<td colspan="'+(wst-wi)+'" class="filler ' + c+'">'+((c=="framename") ? fname : '' )+'</td>');
				}
				if (labels[k]["type"]=="target") {	// target span next to arguments
					if (k>0 && labels[k-1]["start"]==labels[k]["start"] && labels[k-1]["end"]==labels[k]["end"])
						$trN.children().last().addClass("target");
					else if (k>0 && labels[k-1]["start"]<=labels[k]["start"] && labels[k-1]["end"]>=labels[k]["end"]) {
						// partial overlap; don't add a separate cell
					}
/*					else if (k<labels.length-1 && labels[k+1]["start"]<=labels[k]["start"] && labels[k+1]["end"]>=labels[k]["end"]) {
						console.log('partial overlap 2 k='+k+' text='+labels[k]["text"]);
						// partial overlap; don't add a separate cell
					}*/
/*					else if (k<labels.length-1 && labels[k+1]["start"]<labels[k]["end"]) {
						// next span starts after the current one starts but partially overlaps
						// effectively truncate the current span
						wen = labels[k+1]["start"]+1;
						$trN.append('<td colspan="'+(wen-wst)+'" class="target">\xA0</td>');
					}*/
					else {
						$trN.append('<td colspan="'+(wen-wst)+'" class="target w'+wst+':'+wen+'">\xA0</td>');
						if (wst==wen) {
							console.error(wst+' '+wen);
							console.log(labels[k]);
						}
						//console.log('new target span wi='+wi+' wst='+wst+' wen='+wen+' k='+k+' text='+labels[k]["text"]);
					}

					// title text
					var $lastcell = $trN.children().last()
					var oldtitle = $lastcell.attr("title");
					if (oldtitle===undefined) oldtitle = "";
					$lastcell.attr("title", (oldtitle+'\n'+labels[k]["name"]+':\n'+labels[k]["text"]).trim());
				}
				else {	// argument span
					if (k>0 && labels[k-1]["start"]==labels[k]["start"]) {
						if (labels[k-1]["end"]!=labels[k]["end"]) {
							console.error("Unexpected condition: start positions match but end positions do not. k="+k);
							console.log(labels[k-1]);
							console.log(labels[k]);
						}
						$trN.children().last().replaceWith('<td colspan="'+(wen-wst)+'" class="'+$trN.children().last().attr("class")+' arg">'+labels[k]["name"]+'</td>');
						//console.log('replaced k='+k);
					}
					else
						$trN.append('<td colspan="'+(wen-wst)+'" class="arg w'+wst+':'+wen+'">'+labels[k]["name"]+'</td>');

/*					if (k>0 && labels[k-1]["type"]=="target" && labels[k-1]["end"]==labels[k]["start"] && labels[k-1]["continues"])
						$trN.children().last().addClass("target");	// arg span is continuing a target span
*/
					// title text
					var $lastcell = $trN.children().last()
					var oldtitle = $lastcell.attr("title");
					if (oldtitle===undefined) oldtitle = "";
					$lastcell.attr("title", (oldtitle+'\n'+fname+'.'+labels[k]["name"]+':\n'+labels[k]["text"]).trim());
				}
				if (k==0 || k==labels.length-1) {
					if (k==0) $trN.children().last().addClass("leftmost");
					if (k==labels.length-1) $trN.children().last().addClass("rightmost");
					// outermost arg or target
				}
				wi = wen;
			//}
		}

		$trN.addClass("w"+labels[0]["start"]+":"+(maxwen-1));
		$trN.children().addClass('a'+aId).addClass(fTag);

		rows.push($trN);

		aId++;
	};



	if (targets.length>0 && targets.indexOf(0)>-1) {	// Populate the targets row with frame names
		var r=0;
		var $curcell = $('<td></td>');
		var curcolspan = 0;


		$('<td class="filler"></td>').attr("colspan", 1+targets.indexOf(0)).appendTo($trtN);

		// all targets assumed to be contiguous and their IDs to be monotonic
		var curannid = 0;
		while (targets.indexOf(curannid)>-1) {
			if (curannid>0) {
				var colspan = targets.indexOf(curannid)-targets.lastIndexOf(curannid-1)-1;
				if (colspan>0)
					$('<td class="filler"></td>').attr("colspan", colspan).appendTo($trtN);
			}
			$curcell = $('<td id="target-a'+curannid+'" class="framename a'+curannid+'">'+frames[curannid]+'</td>');
			$curcell.attr("colspan", targets.lastIndexOf(curannid)-targets.indexOf(curannid)+1);
			$curcell.appendTo($trtN);
			curannid++;
		}

		$sN.append($trtN);
	}

	// Sort rows by number of tokens in between the outermost words covered by the annotation
	// (i.e. the overall span of the annotation). Break ties by prioritizing rightmost spans.

	rows.sort(function (row1,row2) {
		var aR = getRangeFromClassAttr(new String(row1.attr("class")), "w");
		var al = aR[1]-aR[0];
		var bR = getRangeFromClassAttr(new String(row2.attr("class")), "w");
		var bl = bR[1]-bR[0];
		if (al==bl) return ((aR[0]>bR[0]) ? 1 : -1);
		return 2*(al-bl);
		});


	var grid = [];

	// determine a position for this frame block in the grid
	for (var iR=0; iR<rows.length; iR++) {
		var annspan = getRangeFromClassAttr(new String(rows[iR].attr("class")), "w")
		annspan.push(rows[iR]);
		var matched = false;
		for (var r=0; r<grid.length; r++) {
			matched = true;
			for (var j=0; j<grid[r].length; j++) {
				if (!(grid[r][j][1]<=annspan[0] || annspan[1]<=grid[r][j][0])) {
					// conflicts with a span in this row
					matched = false;
					break;
				}
			}
			if (matched) {	// no conflict in this row
				grid[r].push(annspan);
				break;
			}
		}
		if (!matched)	// start a new row in the grid
			grid.push([annspan]);
	}
	// assemble the grid, merging together non-overlapping frame annotations so they lie in the same row
	for (var r=0; r<grid.length; r++) {
		grid[r].sort(function (a,b) { return a[0]-b[0]; });
		$tr = grid[r][0][2];
		for (var j=1; j<grid[r].length; j++) {
			if (grid[r][j][0]-grid[r][j-1][1]>0)
				$tr.append('<td class="filler" colspan="'+(grid[r][j][0]-grid[r][j-1][1])+'"></td>');
			$tr.append(grid[r][j][2].children().not('.framename'));
		}
		$sN.append($tr);
	}

	return $sN;
}
