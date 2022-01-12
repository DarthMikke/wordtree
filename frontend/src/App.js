import React, { Component } from 'react';
import SearchForm from './SearchForm.js';

class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      search: "",
      typing: false,
      selected: []
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
      image = <img src={pk_query} alt="Genealogical tree" />;
    } else {
      selectedItems = "Vel eit ord frå lista til venstre";
    }
    return (
      <div className="container-sm px-4 p-5 pb-0 pe-lg-0 pt-lg-5 align-items-center rounded-3 border shadow-lg">
        <div className="row">
          <div className="col-6">
            <SearchForm
              selected={ this.state.selected }
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
      </div>
    );
  }
}

export default App;
