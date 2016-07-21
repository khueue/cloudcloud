import {run} from '@cycle/xstream-run';
import {div, label, input, hr, h1, makeDOMDriver} from '@cycle/dom';

function main(sources) {
	const sinks = {
		DOM: sources.DOM.select('.field').events('input')
			.map(ev => ev.target.value)
			.startWith('')
			.map(name =>
				div([
					label('Name:'),
					input('.field', {attrs: {type: 'text'}}),
					hr(),
					h1('Hello ' + name),
				])
			)
	};
	return sinks;
}

run(main, {
	DOM: makeDOMDriver('#app'),
});

/*
'use strict';

var CfnReducer = require('cfn-reducer');

var template = {
	hello: 'test',
};

// Specify necessary parameters.
var stackParams = {
	MyParam1: 'some-value-1',
	MyParam2: 'some-value-2',
};

// Run the reducer.
var options = {
	stackParams: stackParams,
};
var reducer = new CfnReducer(template, options);
var reduced = reducer.reduce();

// Show me the magic!
var output = JSON.stringify(reduced, null, '\t');

setTimeout(function () {
	document.body.innerHTML = output;
}, 500);
*/
