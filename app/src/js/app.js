import {run} from '@cycle/xstream-run';
import xs from 'xstream';
import {makeDOMDriver} from '@cycle/dom';
import {div, textarea, label, br, hr} from '@cycle/dom';
import CfnReducer from 'cfn-reducer';

function main(sources) {
	function reduce(templateText) {
		let reduced = templateText;
		try {
			const template = JSON.parse(templateText);
			const cfnReducer = new CfnReducer(template, {
				stackParams: {
					hello: 'replaced',
				},
			});
			reduced = cfnReducer.reduce();
			reduced = JSON.stringify(reduced, null, '  ');
		} catch (e) {}
		return reduced;
	}

	const startTemplate = JSON.stringify({
		'Fn::Equals': [
			'value',
			'value',
		],
	}, null, '  ');

	const inputTemplate$ = sources.DOM
		.select('#input-template')
		.events('input')
		.map(ev => ev.target.value)
		.startWith(startTemplate);

	const state$ = inputTemplate$.map(inputTemplate => {
		return {
			input: inputTemplate,
			output: reduce(inputTemplate),
		};
	});

	const sinks = {
		DOM: state$.map(state => {
			return div([
				label('Input template'),
				br(),
				textarea('#input-template', {style: {width: '300px', height: '150px'}}, state.input),
				hr(),
				label('Output template'),
				br(),
				textarea('#output-template', {style: {width: '300px', height: '150px'}}, state.output),
			]);
		}),
	};
	return sinks;
}

const drivers = {
	DOM: makeDOMDriver('#app'),
};

run(main, drivers);
