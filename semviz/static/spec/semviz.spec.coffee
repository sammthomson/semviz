###
jasmine unit tests for semviz.coffee

run with jasmine-node (https://github.com/mhevery/jasmine-node)

author Sam Thomson (sthomson@cs.cmu.edu)
###
{SemViz} = require('../coffeescripts/semviz.coffee')

SENTENCE_FIXTURE = {
	"frames": [
     {
       "frame_elements": [
         {
           "start": 7,
           "end": 8,
           "name": "Substance",
           "text": "Materials"
         }
       ],
       "target": {
         "start": 7,
         "end": 8,
         "name": "Substance",
         "text": "Materials"
       }
     },
     {
       "frame_elements": [
         {
           "start": 13,
           "end": 18,
           "name": "Activity",
           "text": "of secret uranium transfer back"
         }
       ],
       "target": {
         "start": 12,
         "end": 13,
         "name": "Activity_finish",
         "text": "completion"
       }
     },
     {
       "frame_elements": [],
       "target": {
         "start": 2,
         "end": 3,
         "name": "Assistance",
         "text": "Helps"
       }
     },
     {
       "frame_elements": [
         {
           "start": 6,
           "end": 7,
           "name": "Situation",
           "text": "Nuclear"
         }
       ],
       "target": {
         "start": 5,
         "end": 6,
         "name": "Risky_situation",
         "text": "Dangerous"
       }
     },
     {
       "frame_elements": [
         {
           "start": 15,
           "end": 16,
           "name": "Substance",
           "text": "uranium"
         },
         {
           "start": 14,
           "end": 15,
           "name": "Descriptor",
           "text": "secret"
         }
       ],
       "target": {
         "start": 15,
         "end": 16,
         "name": "Substance",
         "text": "uranium"
       }
     },
     {
       "frame_elements": [
         {
           "start": 12,
           "end": 18,
           "name": "Message",
           "text": "completion of secret uranium transfer back"
         },
         {
           "start": 9,
           "end": 11,
           "name": "Speaker",
           "text": "Energy agency"
         }
       ],
       "target": {
         "start": 11,
         "end": 12,
         "name": "Statement",
         "text": "announces"
       }
     },
     {
       "frame_elements": [],
       "target": {
         "start": 4,
         "end": 5,
         "name": "Protecting",
         "text": "Secure"
       }
     },
     {
       "frame_elements": [
         {
           "start": 6,
           "end": 7,
           "name": "Weapon",
           "text": "Nuclear"
         }
       ],
       "target": {
         "start": 6,
         "end": 7,
         "name": "Weapon",
         "text": "Nuclear"
       }
     },
     {
       "frame_elements": [
         {
           "start": 15,
           "end": 16,
           "name": "Phenomenon",
           "text": "uranium"
         }
       ],
       "target": {
         "start": 14,
         "end": 15,
         "name": "Secrecy_status",
         "text": "secret"
       }
     },
     {
       "frame_elements": [
         {
           "start": 15,
           "end": 16,
           "name": "Theme",
           "text": "uranium"
         },
         {
           "start": 18,
           "end": 20,
           "name": "Recipient",
           "text": "to Russia"
         }
       ],
       "target": {
         "start": 16,
         "end": 17,
         "name": "Transfer",
         "text": "transfer"
       }
     }
   ],
   "text": [
     "United",
     "States",
     "Helps",
     "Uzbekistan",
     "Secure",
     "Dangerous",
     "Nuclear",
     "Materials",
     ":",
     "Energy",
     "agency",
     "announces",
     "completion",
     "of",
     "secret",
     "uranium",
     "transfer",
     "back",
     "to",
     "Russia"
   ]
}



describe 'SemViz', ->
	viz = new SemViz

	describe 'sortIntoTable', ->
		table = viz.sortIntoTable(SENTENCE_FIXTURE)

		it 'should have numTokens rows', ->
			expect(table.length).toEqual(SENTENCE_FIXTURE.text.length)

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
			contains = (table, cell) ->
				(return true if col?.label == cell.name) for col in row for row in table
				return false

			for frame in SENTENCE_FIXTURE.frames
				for frameElement in frame.frame_elements
					expect(contains(table, frameElement)).toBe(true)

		it 'should have undefineds below multi-token spans', ->
			for row, i in table
				for cell, j in row
					if cell?
						spanLength = cell.spanLength
						if spanLength > 1
							for offset in [1...spanLength]
								# next spanLen - 1 should be undefined
								expect(table[i+offset][j]).toBeUndefined()
