import React, { Component } from 'react';
import _ from './i18n.js';

export default class SearchForm extends Component {
  constructor(props) {
    super(props)

    this.state = {
      input: "",
      words: []
    }
    this.handleInput = this.handleInput.bind(this)
    this.loadWords = this.loadWords.bind(this)
  }

  loadWords(query) {
    fetch(`api/autofill?query=${query}`)
      .then((x) => x.json())
      .then((x) => this.setState({words: x.suggestions}))
  }

  handleInput(event) {
    this.setState({input: event.target.value});
    this.loadWords(event.target.value);
  }

  render() {
    let words = this.state.words.map(x => {
      let button = this.props.selected.findIndex((y) => x.id === y.id ) === -1 ?
        <button className="btn btn-primary btn-sm" onClick={() => this.props.onAdd(x)}>+</button> :
        <></>
      return <div className="row" key={x.id}>
        <div className="col">{x.word} <small>({x.language})</small></div>
        <div className="col">{button}</div>
      </div>
    })
    return <>
      <form>
        <input
          className="form-control"
          key="input"
          type="text"
          /* style={{width: "4em"}} */
          id="query"
          value={this.state.input}
          onChange={this.handleInput}
          placeholder={_('Type here to search', this.props.lang)} />
      </form>
      <div className="container">
        {words}
      </div>
    </>
  }
}
