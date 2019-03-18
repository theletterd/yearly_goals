/*
'use strict';

const e = React.createElement;

class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return e(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'Like'
    );
  }
}

class YearlyGoals extends React.Component {
    constructor(props) {
	super(props);
	this.state = {
	    year: 1983
	};
    }
    
    componentDidMount() {
	fetch("0.0.0.0:5000")
    }

    render() {
	return (
	  <div>{this.state.year}</div>
	);
    }
}
*/
//const domContainer = document.querySelector('#like_button_container');
//ReactDOM.render(e(LikeButton), domContainer);


/*
ReactDOM.render(
  <YearlyGoals />,
  document.getElementById('yearlyGoals')
);

*/
