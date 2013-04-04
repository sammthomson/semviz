###
jasmine unit tests for semviz.coffee

run with jasmine-node (https://github.com/mhevery/jasmine-node)

author Sam Thomson (sthomson@cs.cmu.edu)
###
{SemViz} = require('../coffeescripts/semviz.coffee')

SENTENCE_FIXTURE = {
  "frames": [
    {
    "target": {
    "start": 2,
    "end": 4,
    "name": "Temporal_collocation",
    "text": "no longer"
    },
    "annotationSets": [
      {
      "frameElements": [],
      "score": 38.67659171230181,
      "rank": 0
      }
    ]
    },
    {
    "target": {
    "start": 1,
    "end": 2,
    "name": "Building_subparts",
    "text": "kitchen"
    },
    "annotationSets": [
      {
      "frameElements": [
        {
        "start": 1,
        "end": 2,
        "name": "Building_part",
        "text": "kitchen"
        },
        {
        "start": 0,
        "end": 1,
        "name": "Whole",
        "text": "My"
        }
      ],
      "score": 18.21350901550272,
      "rank": 0
      }
    ]
    },
    {
    "target": {
    "start": 4,
    "end": 5,
    "name": "Sensation",
    "text": "smells"
    },
    "annotationSets": [
      {
      "frameElements": [],
      "score": 36.702918021406155,
      "rank": 0
      }
    ]
    }
  ],
  "tokens": [
    "My",
    "kitchen",
    "no",
    "longer",
    "smells",
    "."
  ]
}


describe 'SemViz', ->
	viz = new SemViz

	describe 'sortIntoTable', ->
		table = viz.sortIntoTable(SENTENCE_FIXTURE)

		it 'should have numTokens rows', ->
			expect(table.length).toEqual(SENTENCE_FIXTURE.tokens.length)

		it 'should have numFrames columns', ->
			expect(table[0].length).toEqual(SENTENCE_FIXTURE.frames.length)

		it 'should contain every target', ->
			tableTargets = {}
			for row in table
				for cell in row
					if cell?.isTarget
						tableTargets[cell.label] = 1

			sentenceTargets = {}
			for frame in SENTENCE_FIXTURE.frames
				sentenceTargets[frame.target.name] = 1

			expect(tableTargets).toEqual(sentenceTargets)

		it 'should contain every frame element', ->
			# TODO: some FEs actually get overwritten, this only works because
			#       because the target that overwrites it has the same label :(
			contains = (table, frameElementName) ->
				(return true if col?.label == frameElementName.name) for col in row for row in table
				return false

			for frame in SENTENCE_FIXTURE.frames
				for frameElement in frame.annotationSets[0].frameElements
					expect(contains(table, frameElement.name)).toBe(true)

		it 'should have undefineds below multi-token spans', ->
			for row, i in table
				for cell, j in row
					if cell?
						spanLength = cell.spanLength
						if spanLength > 1
							for offset in [1...spanLength]
								# next spanLen - 1 should be undefined
								expect(table[i+offset][j]).toBeUndefined()
