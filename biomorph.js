
//http://www.emergentmind.com/biomorphs



var CANVAS_HEIGHT = 148;                    // Factors in the 2px border
var CANVAS_WIDTH = 318;                     // Factors in the 2px border
var NUM_CHILDREN = 8;
var DEFAULT_COLOR = '#000';
var HOVER_COLOR = '#CD4C2C';
var GENE_MAX_INDEX = 8;
var GENE_MUTATION_DELTA = 2;
var GENE_RANGE_DIMENSION = [ -9, 9 ];
var GENE_RANGE_DEPTH = [ 3, 9 ]

var EXAMPLES = [
    [ 'Bug', [ 1, -2, 3, 4, -5, 1, -2, -3, 8 ] ],
    [ 'Antlers', [ -2, -6, -1, 2, -5, -5, -1, -3, 7] ],
    [ 'Spaceship', [ -2, 9, -3, 4, 4, 7, 2, 0, 6 ] ],
    [ 'Frog', [ -4, 1, 4, 1, 4, 9, -9, 5, 6 ] ],
    [ 'Medusa', [ -4, 2, 1, 3, -7, -3, -1, 8, 7 ] ],
];

//
// Generates a random number in a range
function random( low, high ) {
    return low + Math.floor( Math.random() * ( high - low ) );
}

$( function() {

    if ( ! checkForCanvasSupport() ) {
        $( 'div#panel' ).hide();
        return;
    }

    function Biomorph( genes, $canvas ) {
        this.$canvas = $canvas;
        this.ctx = this.$canvas.get( 0 ).getContext( '2d' );
        this.getDimensionsFromCanvas();
        this.setGenes( genes );
        this.setColor( DEFAULT_COLOR );
        this.children = [];
        this.clearDimensions();
        this.enabled = true;
    }

    Biomorph.prototype = {

        setGenes: function( genes ) {
            this.genes = genes;
        },

        setColor: function( color ) {
            this.color = color;
        },

        resetChildren: function() {
            for( var i = 0; i < NUM_CHILDREN; i++ ) {
                var $canvas = $( 'canvas#child_' + i );
                var biomorphChild = new Biomorph( [], $canvas );
                biomorphChild.render();
            }
        },

        getDimensionsFromCanvas: function() {
            this.canvasHeight = this.$canvas.height();
            this.canvasWidth = this.$canvas.width();
        },

        clear: function() {
            this.ctx.clearRect( 0, 0, this.canvasWidth, this.canvasHeight );
        },

        renderLine: function( x1, y1, x2, y2 ) {
            this.ctx.strokeStyle = this.color;
            this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.moveTo( x1, y1 + this.yOffset );
        this.ctx.lineTo( x2, y2 + this.yOffset );
        this.ctx.stroke();
        },

        trackDimensions: function( x1, y1, x2, y2 ) {

            if ( null === this.xMin || x1 < this.xMin ) {
                this.xMin = x1;
            }

            if ( null === this.xMin || x2 < this.xMin ) {
                this.xMin = x2;
            }

            if ( null === this.xMax || x1 > this.xMax ) {
                this.xMax = x1;
            }

            if ( null === this.xMax || x2 > this.xMax ) {
                this.xMax = x2;
            }

            if ( null === this.yMin || y1 < this.yMin ) {
                this.yMin = y1;
            }

            if ( null === this.yMin || y2 < this.yMin ) {
                this.yMin = y2;
            }

            if ( null === this.yMax || y1 > this.yMax ) {
                this.yMax = y1;
            }

            if ( null === this.yMax || y2 > this.yMax ) {
                this.yMax = y2;
            }
        },

        getRenderedHeight: function() {
            return this.yMax - this.yMin;
        },

        getRenderedWidth: function() {
            return this.xMax - this.xMin;
        },

        isWithinCanvas: function() {
            return this.getRenderedHeight() < this.canvasHeight && this.getRenderedWidth() < this.canvasWidth;
        },

        getCenterY: function() {
            return (this.yMax + this.yMin) / 2;
        },

        isFirstRender: function() {
            return ( null === this.xMin || null === this.xMax || null === this.yMin || null === this.yMax );
        },

        tree: function( x1, y1, depth, geneIndex ) {

        var x2 = x1 + depth * this.getXOffsets()[ geneIndex ];
        var y2 = y1 + depth * this.getYOffsets()[ geneIndex ];

            this.renderLine( x1, y1, x2, y2 );
            this.trackDimensions( x1, y1, x2, y2 );

        if ( depth > 0 ) {
          this.tree( x2, y2, depth - 1, ( geneIndex + ( GENE_MAX_INDEX - 1) ) % GENE_MAX_INDEX );
          this.tree( x2, y2, depth - 1, ( geneIndex + 1 ) % GENE_MAX_INDEX );
        }
        },

        render: function( isFirstRun ) {

        this.clear();

            if ( isFirstRun ) {
                this.yOffset = 0;
            } else {
                this.yOffset = ( this.canvasHeight / 2 ) - this.getCenterY();
            }

        this.tree( this.canvasWidth / 2, this.canvasHeight / 2, this.genes[ GENE_MAX_INDEX ], 2 );
        },

        renderAndCenter: function() {

            // We render it once in order to get the yMin and yMax coordinates
            this.render( true );

            // Then using that information we render it with an offset to center it vertically
            this.render( false );
        },

        getXOffsets: function() {
        return [ -this.genes[1], -this.genes[0], 0, this.genes[0], this.genes[1], this.genes[2], 0, -this.genes[2] ];
        },

        getYOffsets: function() {
        return [ this.genes[5], this.genes[4], this.genes[3], this.genes[4], this.genes[5], this.genes[6], this.genes[7], this.genes[6] ];
        },

        decrementDepth: function() {
            this.genes[ GENE_MAX_INDEX ]--;
        },

        clearDimensions: function() {
            this.xMin = null;
            this.xMax = null;
            this.yMin = null;
            this.yMax = null;
        },

        disable: function() {
            this.enabled = false;
            this.color = '#ccc';
            this.renderAndCenter();
        },

        renderChildren: function() {
            for( var i = 0; i < NUM_CHILDREN; i++ ) {
                var $canvas = $( 'canvas#child_' + i );

                // Need the .slice() call so that it creates a copy of the parent's genes array
                var biomorphChild = new Biomorph( this.genes.slice(), $canvas );

                biomorphChild.mutate();
                biomorphChild.renderAndCenter();

                // We check whether the child is too big for the canvas and if so, shrink it
                if ( ! biomorphChild.isWithinCanvas() ) {
                    biomorphChild.disable();
                }

                this.children[i] = biomorphChild;
            }
        },

        isGeneValueInRange: function( geneIndex, geneValue ) {
            if ( geneIndex < GENE_MAX_INDEX ) {
                return geneValue >= GENE_RANGE_DIMENSION[ 0 ] && geneValue <= GENE_RANGE_DIMENSION[ 1 ];
            } else if ( GENE_MAX_INDEX == geneIndex ) {
                return geneValue >= GENE_RANGE_DEPTH[ 0 ] && geneValue <= GENE_RANGE_DEPTH[ 1 ];
            }
        },

        mutate: function() {
            do {

                // Ensure a small change the genes
                do {
                    var mutationOffset = random( -GENE_MUTATION_DELTA, GENE_MUTATION_DELTA );
                } while ( 0 === mutationOffset );

                var geneIndex = random( 0, GENE_MAX_INDEX );
                var newValue = this.genes[ geneIndex ] + mutationOffset;

            } while ( ! this.isGeneValueInRange( geneIndex, newValue ) );

            this.genes[ geneIndex ] = newValue;
        },

        setSliderGeneValues: function() {
            for( var i = 0; i < this.genes.length; i++ ) {
                var $geneContainer = $( 'div#genes' ).find( 'div#gene_' + i );
                $geneContainer.find( 'div.slider' ).slider( 'value', this.genes[ i ] );
                $geneContainer.find( 'span.value' ).text( this.genes[ i ] );
            }
        },

        startEditing: function() {
            this.editing = true;
        },

        endEditing: function() {
            this.editing = false;
        },

        isEditing: function() {
            return this.editing;
        },

        setGenesFromSliderAndRender: function() {
            var newGenes = [];
            for( var i = 0; i < parentBiomorph.genes.length; i++ ) {
                var geneValue = $( 'div#genes' ).find( 'div#gene_' + i ).find( 'div.slider' ).slider( 'value' );
                newGenes.push( geneValue );
            }

            this.setGenes( newGenes );
            this.clearDimensions();
            this.renderAndCenter();
        }
    }

    // Set the dimensions of all the biomorphs
    $( 'div#biomorphs' ).find( 'canvas' ).attr( 'height', CANVAS_HEIGHT ).attr( 'width', CANVAS_WIDTH );

    var parentBiomorph = new Biomorph( EXAMPLES[ 3 ][ 1 ], $( 'canvas#parent' ) );
    parentBiomorph.renderAndCenter();
    parentBiomorph.renderChildren();

    //
    // Triggered when the user modifies the parent biomorph's genes
    function updateParentFromSlider( event, ui ) {
        $( this ).parent().find( 'span.value' ).text( ui.value );

        // ui.value represents the value that the slider is about to be
        // Therefore we need to set the slider's value to this now so that
        // the gene values are correct when it is rendered
        $( this ).parent().find( 'div.slider' ).slider( 'value', ui.value );

        parentBiomorph.setGenesFromSliderAndRender();
    }

    //
    // Initialize the gene dimensions sliders
    $( 'div#genes div.slider.dimensions' ).slider({
        min: GENE_RANGE_DIMENSION[ 0 ],
        max: GENE_RANGE_DIMENSION[ 1 ],
        slide: updateParentFromSlider
    });

    //
    // Initialize the gene depth slider
    $( 'div#genes div.slider.depth' ).slider({
        min: GENE_RANGE_DEPTH[ 0 ],
        max: GENE_RANGE_DEPTH[ 1 ],
        slide: updateParentFromSlider
    });

    //
    // User clicks on of the children to make it the parent
    $( 'canvas.child' ).on( 'click', function( e ) {

        if ( parentBiomorph.isEditing() ) {
            return;
        }

        var childIndex = +$( this ).attr( 'id' ).substring( 'child_'.length );
        if ( ! parentBiomorph.children[ childIndex ].enabled ) {
            var $sizeAlert = jQuery('<div id="size_alert">Too large</div>');
            $sizeAlert.addClass( 'unselectable' );
            $sizeAlert.css( {
                color: '#C36363',
                fontWeight: 'bold',
                fontSize: '18px',
                position: 'absolute',
                left: $( this ).position().left,
                top: $( this ).position().top + ( $( this ).height() - $sizeAlert.height() ) / 2,
                width: $( this ).width(),
                textAlign: 'center',
            } );


            $sizeAlert.insertAfter( $( this ) ).fadeOut();
            return;
        }

        parentBiomorph = new Biomorph( parentBiomorph.children[ childIndex ].genes, $( 'canvas#parent' ) );
        parentBiomorph.renderAndCenter();
        parentBiomorph.renderChildren();

    }).on( 'mousemove', function( e ) {

        if ( parentBiomorph.isEditing() ) {
            return;
        }

        var childIndex = +$( this ).attr( 'id' ).substring( 'child_'.length );
        if ( ! parentBiomorph.children[ childIndex ].enabled ) {
            return;
        }

        parentBiomorph.children[ childIndex ].setColor( HOVER_COLOR );
        parentBiomorph.children[ childIndex ].renderAndCenter();
        $( this ).addClass( 'hover' );

    }).on( 'mouseleave', function( e ) {

        if ( parentBiomorph.isEditing() ) {
            return;
        }

        var childIndex = +$( this ).attr( 'id' ).substring( 'child_'.length );
        if ( ! parentBiomorph.children[ childIndex ].enabled ) {
            return;
        }

        parentBiomorph.children[ childIndex ].setColor( DEFAULT_COLOR );
        parentBiomorph.children[ childIndex ].renderAndCenter();
        $( this ).removeClass( 'hover' );

    });

    //
    // User is done editing the parent biomorh's genes
    function endEditing() {
        var $genes = $( 'div#genes' );
        $genes.fadeOut(100);
        parentBiomorph.renderChildren();
        parentBiomorph.endEditing();
    }

    //
    // When the user clicks outside of the gene modification window, hide it
    $( 'body' ).on( 'click', function( e ) {
        if ( $( 'div#genes' ).is( ':visible' ) ) {
            endEditing();
        }
    });

    //
    // We don't want the click propogating up to the body (which would hide the gene modification window)
    $( 'div#genes' ).on( 'click', function( e ) {
        e.stopPropagation();
    });

    $( 'a#edit' ).on( 'click', function( e ) {

        parentBiomorph.setSliderGeneValues();

        var $parentContainer = $( this ).parent();
        var $genes = $( 'div#genes' );

        if ( $genes.is( ':visible' ) ) {
            endEditing();
        } else {
            parentBiomorph.resetChildren();
            parentBiomorph.startEditing();

            $genes.show();
            $genes.css({
                left: $parentContainer.position().left,
                top: $parentContainer.position().top + $parentContainer.height()
            });
        }

        return false;
    });

    //
    // User clicks on one of the example biomoprhs
    $( 'div#examples' ).on( 'click', 'canvas', function( e ) {

        var exampleIndex = +$( this ).attr( 'id' ).substring( 'example_'.length );
        var exampleGenes = EXAMPLES[ exampleIndex ][ 1 ];

        parentBiomorph = new Biomorph( exampleGenes, $( 'canvas#parent' ) );
        parentBiomorph.renderAndCenter();
        parentBiomorph.renderChildren();
    });

    function renderExamples() {

        var $examples = $( 'div#examples' );

        for( var i = 0; i < EXAMPLES.length; i++ ) {
            var exampleName = EXAMPLES[ i ][ 0 ];
            var exampleGenes = EXAMPLES[ i ][ 1 ]

            // Create the element
            var $exampleContainer = $( '<div class="example_container"></div>' );
            $exampleContainer.css( {width: CANVAS_WIDTH} );

            var $exampleName = $( '<div class="name"></div>').text( exampleName );
            var $exampleCanvas = $( '<canvas></canvas>' );
            $exampleCanvas.attr( { width: CANVAS_WIDTH, height: CANVAS_HEIGHT, id: 'example_' + i } );

            $exampleContainer.append( $exampleName ).append( $exampleCanvas );
            $examples.append( $exampleContainer );

            // Render the biomorph
            var biomorph = new Biomorph( exampleGenes, $exampleCanvas );
            biomorph.setColor( 'white' );
            biomorph.renderAndCenter();

            // Adjust the width of the element based on the width of the biomorph
            var renderedWidth = biomorph.getRenderedWidth();
            $exampleContainer.css( { width: renderedWidth } );
            $exampleCanvas.attr( { width: renderedWidth } );

            // Finally, re-render the biomorph on the resized canvas
            biomorph.getDimensionsFromCanvas();
            biomorph.renderAndCenter();
        }
    }

    renderExamples();
});
