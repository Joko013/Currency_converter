import json
import click
from flask import Flask, request, jsonify
from converter import Converter

app = Flask(__name__)
c = Converter()


@click.command()
@click.option('--amount', type=float, help="Amount to be converted.")
@click.option('--input_currency', help="Input currency code or symbol.")
@click.option('--output_currency', default=None, help="Output currency code or symbol.")
def call_convert_currency_cli(amount, input_currency, output_currency):
    click.echo(json.dumps(c.convert_currency(amount, input_currency, output_currency), indent=4))


@app.route('/currency_converter', methods=["GET"])
def call_convert_currency_api():
    amount = request.args.get('amount')
    input_currency = request.args.get('input_currency', type=str)
    output_currency = request.args.get('output_currency', type=str)
    return jsonify(c.convert_currency(amount, input_currency, output_currency))


if __name__ == '__main__':
    call_convert_currency_cli()





