import argparse
import json
import yaml
from loguru import logger
from hil.core import Cantp, UdsClient
from hil.core.doip_client import DoipClient
from hil.bus import load_bus
from hil.common.utils import parser_canid


__version__ = '1.0.0'
__author__ = 'notmmao@gmail.com'

def load_config(fn:str):
    with open(fn, "r", encoding="utf-8") as f:
        if fn.endswith(".json"):
            config = json.load(f)
        else:
            config = yaml.safe_load(f)
        return config

def uds(txid, rxid, cmd_config:str, bus_config:str, extended=False):
    txid = parser_canid(txid)
    rxid = parser_canid(rxid)
    bus = load_bus(bus_config)
    tp = Cantp(bus, txid, rxid, is_extended_id=extended)
    client = UdsClient()
    cmds = load_config(cmd_config)
    ctx = {}
    client.run(cmds, tp, ctx, 3)
    bus.shutdown()
    return ctx

def doip(doip_config:str, cmd_config:str):
    cmds = load_config(cmd_config)
    config = load_config(doip_config)
    tp = DoipClient(**config)
    client = UdsClient()
    ctx = {}
    client.run(cmds, tp, ctx, 3)
    return ctx

def main():
    logger.enable("hil.core")

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="protocol")
    can_parser = subparsers.add_parser("can")
    can_parser.add_argument("--txid", "-t", required=True, help="请求CANID")
    can_parser.add_argument("--rxid", "-r", required=True, help="接收CANID")
    can_parser.add_argument("--cmd", "-c", required=True, help="命令序列json或yaml文件")
    can_parser.add_argument("--bus", "-b", required=True, help="CAN总线配置json或yaml文件")
    can_parser.add_argument("--extended", "-e", action="store_true", help="CAN扩展帧")
    
    doip_parser = can_parser = subparsers.add_parser("doip")
    can_parser.add_argument("--node", "-n", required=True, help="DoIP配置yaml文件")
    doip_parser.add_argument("--cmd", "-c", required=True, help="命令序列json或yaml文件")

    args = parser.parse_args()
    logger.debug(args)
    if args.protocol == "doip":
        ctx = doip(args.node, args.cmd)
        logger.info(ctx)
    elif args.protocol == "can":
        ctx = uds(args.txid, args.rxid, args.cmd, args.bus, args.extended)
        logger.info(ctx)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()