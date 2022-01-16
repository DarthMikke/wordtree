import React, { Component } from 'react';
import SearchForm from './SearchForm.js';
import _ from './i18n.js';

class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      search: "",
      typing: false,
      selected: [],
      lang: 'nn',
    }
    this.select = this.select.bind(this);
    this.unselect = this.unselect.bind(this);
  }

  select(word) {
    let selected = this.state.selected;
    selected.push(word);
    this.setState({selected: selected})
  }

  unselect(pk) {
    let selected = this.state.selected;
    let index = selected.findIndex(x => x.id === pk);
    console.log(`Removing ${index}`);
    selected.splice(index, 1);
    this.setState({selected: selected})
  }

  render() {
    let selectedItems
    let image = null;
    if (this.state.selected.length > 0) {
      selectedItems = this.state.selected.map((x) => {
        console.log(x)
        return <span key={x.id}>{x.word} <small>({x.language})</small> <button className="btn btn-secondary btn-sm" onClick={() => this.unselect(x.id)}>-</button></span>
      })
      let pk_query = `image/${this.state.selected.map((x) => x.id)
        .reduce((a, b) => a.toString() + "," + b.toString())
      }.png`;
      image = <img style={{maxWidth: "100%"}} src={pk_query} alt="Genealogical tree" />;
    } else {
      selectedItems = _('Choose a word from list to the left', this.state.lang);
    }
    return (
      <div className="container-sm px-4 p-5 pb-0 pe-lg-0 pt-lg-5 align-middle rounded-3 border shadow-lg">
        <div className="text-center row pb-3">
          <p>
          <span><a href="#" onClick={() => this.setState({lang: 'en'})}>🇬🇧See this in English</a></span>&nbsp;|&nbsp;
          <span><a href="#" onClick={() => this.setState({lang: 'nn'})}>🇳🇴Sjå dette på norsk</a></span>
          </p>
        </div>
        <h1>Wordtree</h1>
        <div className="row mt-4">
          <div className="col-6">
            <SearchForm
              selected={ this.state.selected }
              lang={this.state.lang}
              isEditing={ (state) => {this.setState({typing: state})} }
              onAdd={ (pk) => this.select(pk) } />
          </div>
          <div className="col-6">
            <p>
            {selectedItems}
            </p>
            {image}
          </div>
        </div>
        <div className="text-center row footer justify-content-center mb-2 mt-4 mute">
          <p className="">{_('Copyright notice', this.state.lang)}</p>
          <p>{_('Read more', this.state.lang)}</p>
        </div>
      </div>
    );
  }
}

export default App;
